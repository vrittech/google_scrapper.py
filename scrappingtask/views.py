from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from playwright.async_api import async_playwright
from script.detailsscraping import scrape_website  # Import scraping logic
from .tasks import save_web_scraping_result  # Import the Celery task
from .models import WebScrapingTask
import logging
from webscrape.throttle import PlanBasedThrottle
from rest_framework.decorators import throttle_classes

# Configure logger
logger = logging.getLogger(__name__)

class WebsiteContactScrapingAPI(APIView):
    """
    API View to scrape websites for contact information and save results using Celery.
    """
    throttle_classes = [PlanBasedThrottle]  # Apply the custom PlanBasedThrottle to limit requests per user based on their plan.

    def get(self, request):
        """
        Handle GET requests to render the form or process scraping.
        """
        # Retrieve websites from query parameters
        websites = request.GET.get("websites", "")

        # If no websites are provided, render the form
        if not websites:
            return render(request, "website_contact_form.html")

        # Split the websites into a list
        website_list = [website.strip() for website in websites.split(",") if website.strip()]
        if not website_list:
            logger.error("Invalid website URLs provided.")
            return Response(
                {"error": "Please provide valid website URLs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Define the asynchronous scraping logic
        async def scrape_all_websites(website_list):
            """
            Asynchronous function to scrape all websites in the provided list.
            """
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                try:
                    results = []
                    for website in website_list:
                        try:
                            logger.info(f"Scraping website: {website}")
                            # Perform scraping for each website
                            result = await scrape_website(website, browser)
                            results.append({"website": website, "contact_info": result})
                        except Exception as e:
                            logger.error(f"Error scraping {website}: {e}")
                            results.append({"website": website, "error": str(e)})
                    return results
                finally:
                    await browser.close()

        # Perform scraping
        try:
            # Create a WebScrapingTask instance for each website
            tasks = []
            for website in website_list:
                task = WebScrapingTask.objects.create(
                    user=request.user,  # Assuming the user is authenticated
                    target_url=website,
                    status="Pending",
                )
                tasks.append(task)

            # Perform scraping asynchronously
            raw_results = async_to_sync(scrape_all_websites)(website_list)

            # Trigger Celery tasks to save results
            for task, result in zip(tasks, raw_results):
                save_web_scraping_result.delay(task.id, result)

            # Return success response
            return Response(
                {
                    "message": "Scraping completed. Results are being saved asynchronously.",
                    "tasks": [{"task_id": task.id, "target_url": task.target_url, "status": task.status} for task in tasks],
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {e}")
            # Return error response in case of failure
            return Response(
                {"error": "An unexpected error occurred during scraping.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def process_results(results):
        """
        Optional: Process raw results to format them.
        """
        processed = []
        for result in results:
            if "error" in result:
                processed.append({"website": result.get("website"), "status": "Error", "details": result.get("error")})
            else:
                processed.append({"website": result.get("website"), "contact_info": result.get("contact_info")})
        return processed