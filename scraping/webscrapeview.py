from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from playwright.async_api import async_playwright
from script.detailsscraping import scrape_website  # Import scraping logic


class WebsiteContactScrapingAPI(APIView):
    """
    API View to scrape websites for contact information.
    """

    def get(self, request):
        """
        Handle GET requests to render the form or process scraping.
        """
        # If no websites are provided, render the form
        websites = request.GET.get("websites", "")
        if not websites:
            return render(request, "website_contact_form.html")

        # Split the websites into a list
        website_list = [website.strip() for website in websites.split(",") if website.strip()]
        if not website_list:
            return Response({"error": "Please provide valid website URLs."}, status=status.HTTP_400_BAD_REQUEST)

        # Define the asynchronous scraping logic
        async def scrape_all_websites():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                try:
                    results = [await scrape_website(website, browser) for website in website_list]
                finally:
                    await browser.close()
                return results

        # Perform scraping
        try:
            raw_results = async_to_sync(scrape_all_websites)()

            # Return raw results as JSON
            return Response(raw_results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
