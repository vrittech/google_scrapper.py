import logging
import time
from threading import Thread
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from playwright.async_api import async_playwright
from script.map_scraper import scrape_visible_listings
import asyncio
from asyncio import Semaphore
import queue

# Configure logging
logging.basicConfig(
    filename='scraping_debug.log',  # File where logs will be saved
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

SEMAPHORE_LIMIT = 5  # Limit the number of concurrent scraping tasks

class GoogleMapScrapingAPI(APIView):
    def get(self, request):
        start_time = time.time()
        logging.info("Received GET request.")

        if not request.GET:
            logging.info("No query parameters found. Rendering HTML form.")
            return render(request, "google_map_scraper_form.html")

        # Retrieve query parameters
        keywords = request.GET.get("search_query", "").strip()
        country = request.GET.get("country", "").strip()
        district = request.GET.get("district", "").strip()
        google_map_link = request.GET.get("google_map_link", "").strip()

        try:
            unique_results_required = int(request.GET.get("results", 10))
            logging.debug(f"User requested {unique_results_required} unique results per keyword.")
        except ValueError:
            logging.error("Invalid 'results' parameter provided.")
            return Response({"error": "Invalid 'results' parameter. It must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if not keywords and not google_map_link:
            logging.error("Validation failed: No search query or Google Map link provided.")
            return Response({"error": "Either 'search_query' or 'google_map_link' is required."}, status=status.HTTP_400_BAD_REQUEST)

        keyword_list = [keyword.strip() for keyword in keywords.split(",") if keyword.strip()]
        logging.info(f"Parsed keywords: {keyword_list}")

        result_queue = queue.Queue()
        semaphore = Semaphore(SEMAPHORE_LIMIT)

        async def scrape_google_maps_with_page(page, keyword):
            logging.info(f"Starting scraping for keyword: {keyword}")
            scraped_data = []
            visited_names = set()

            try:
                # Open Google Maps and perform the search
                if google_map_link:
                    await page.goto(google_map_link, timeout=15000)
                else:
                    search_query = f"{keyword} in {district}, {country}" if district or country else keyword
                    await page.goto("https://www.google.com/maps", timeout=15000)
                    await page.fill('//input[@id="searchboxinput"]', search_query)
                    await page.keyboard.press("Enter")
                    await page.wait_for_selector('//div[contains(@class, "Nv2PK")]', timeout=10000)

                # Set larger viewport size for more visible listings
                await page.set_viewport_size({"width": 1920, "height": 1080})

                # Scroll-to-bottom logic
                for scroll_attempt in range(50):  # Reduce scroll attempts
                    if len(scraped_data) >= unique_results_required:
                        logging.info(f"Required results scraped for keyword: {keyword}")
                        break

                    logging.debug(f"Scrolling attempt {scroll_attempt + 1}. Current results: {len(scraped_data)}")
                    previous_count = len(scraped_data)

                    # Scroll the page
                    await page.evaluate("window.scrollBy(0, 1000)")  # Scroll larger distance
                    await asyncio.sleep(1)  # Reduce delay

                    # Scrape visible listings
                    await scrape_visible_listings(page, unique_results_required, scraped_data, visited_names)

                    # Check if new results have loaded
                    if len(scraped_data) == previous_count:
                        logging.info("No new results loaded. Stopping scrolling.")
                        break

            except Exception as e:
                logging.error(f"Error while scraping '{keyword}': {str(e)}")

            return scraped_data

        async def scrape_keyword(keyword):
            async with semaphore:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
                    context = await browser.new_context()
                    page = await context.new_page()
                    result = await scrape_google_maps_with_page(page, keyword)
                    await browser.close()
                    result_queue.put({keyword: result})

        def thread_worker():
            asyncio.run(scrape_all_keywords())

        async def scrape_all_keywords():
            # Launch browsers for multiple keywords in parallel
            tasks = [scrape_keyword(keyword) for keyword in keyword_list]
            await asyncio.gather(*tasks)

        # Spawn threads for parallel execution
        threads = []
        for _ in range(SEMAPHORE_LIMIT):  # Adjust based on system resources
            thread = Thread(target=thread_worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Aggregate results
        final_results = {}
        while not result_queue.empty():
            final_results.update(result_queue.get())

        elapsed_time = time.time() - start_time
        logging.info(f"All keywords scraped successfully. Total time taken: {elapsed_time:.2f} seconds.")
        return Response(final_results, status=status.HTTP_200_OK)
