import asyncio
from playwright.async_api import async_playwright
import json
import time


async def extract_data(page, xpath):
    """Extract data for a given XPath."""
    try:
        elements = await page.locator(xpath).all_inner_texts()
        return elements[0].strip() if elements else "Not Available"
    except Exception:
        return "Not Available"


async def scrape_listing(page, base_xpath, scraped_data, visited_names):
    """Scrape data from a single listing."""
    try:
        name = await extract_data(page, f'{base_xpath}//div[contains(@class, "fontHeadlineSmall")]')
        if not name or name in visited_names:
            return

        # Click to open details
        await page.locator(base_xpath).click()
        await page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]', timeout=15000)

        # Extract details
        name = await extract_data(page, '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')
        address = await extract_data(page, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]')
        website = await extract_data(page, '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]')
        phone = await extract_data(page, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]')
        reviews_count = await extract_data(page, '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]')
        reviews_average = await extract_data(page, '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]')
        business_category = await extract_data(page, '//div[@class="LBgpqf"]//button[@class="DkEaL "]')
        google_map_link = page.url

        unique_key = f"{name}-{address}"
        if unique_key in visited_names:
            return

        # Append to results and mark as visited
        scraped_data.append({
            "Name": name,
            "Address": address,
            "Website": website,
            "Phone Number": phone,
            "Reviews Count": reviews_count,
            "Average Review Rating": reviews_average,
            "Business Category": business_category,
            "Google Map Link": google_map_link,
        })
        visited_names.add(unique_key)

        # Close details view
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)

    except Exception:
        pass


async def scrape_visible_listings(page, unique_results_required, scraped_data, visited_names):
    """Scrape visible listings asynchronously."""
    listings = await page.locator('//div[contains(@class, "Nv2PK")]').all()
    tasks = []

    for i, locator in enumerate(listings):
        if len(scraped_data) >= unique_results_required:
            break

        base_xpath = f'(//div[contains(@class, "Nv2PK")])[{i + 1}]'
        tasks.append(scrape_listing(page, base_xpath, scraped_data, visited_names))

    if tasks:
        await asyncio.gather(*tasks)


async def main():
    search_query = input("Enter search query (e.g., restaurants near me): ").strip()
    unique_results_required = int(input("Enter number of unique results to scrape: ").strip())
    max_scroll_attempts = 50  # Maximum number of scrolling attempts
    headless_mode = True

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_mode, args=["--disable-images", "--disable-fonts"])
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to Google Maps
            await page.goto("https://www.google.com/maps", timeout=60000)

            # Search for the query
            await page.locator('//input[@id="searchboxinput"]').fill(search_query)
            await page.keyboard.press("Enter")
            await page.wait_for_selector('//div[contains(@class, "Nv2PK")]', timeout=20000)

            scraped_data = []
            visited_names = set()
            scroll_attempts = 0
            start_time = time.time()
            timeout = 300  # Timeout in seconds

            while len(scraped_data) < unique_results_required and scroll_attempts < max_scroll_attempts:
                if time.time() - start_time > timeout:
                    break

                await scrape_visible_listings(page, unique_results_required, scraped_data, visited_names)

                if len(scraped_data) >= unique_results_required:
                    break

                await page.mouse.wheel(0, 3000)
                await asyncio.sleep(2)  # Allow time for additional listings to load
                scroll_attempts += 1

            # Retry with a broader query if results are insufficient
            if len(scraped_data) < unique_results_required:
                await page.locator('//input[@id="searchboxinput"]').fill("Hotels in Bangladesh")
                await page.keyboard.press("Enter")
                await asyncio.sleep(5)
                await scrape_visible_listings(page, unique_results_required, scraped_data, visited_names)

            # Ensure enough unique results are saved
            if len(scraped_data) < unique_results_required:
                print(f"Warning: Only {len(scraped_data)} unique results found.")

            # Save results to JSON
            with open("scraped_data.json", "w", encoding="utf-8") as file:
                json.dump(scraped_data, file, ensure_ascii=False, indent=4)

        finally:
            await browser.close()


# if __name__ == "__main__":
#     asyncio.run(main())
