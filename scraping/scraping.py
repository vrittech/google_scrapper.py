from src.gmaps import Gmaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

@csrf_exempt
def scrape_view(request):
    """
    Handle scraping requests from the frontend form.
    """
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the request
            keywords = data.get("keywords", [])
            locations = data.get("locations", [])
            max_results = int(data.get("max_results", 10))
            scrape_reviews = data.get("scrape_reviews", False)
            convert_to_english = data.get("convert_to_english", True)
            api_key = data.get("api_key", None)
            lang = data.get("lang", None)
            fields = data.get("fields", [])  # New field extraction

            # Validate the required fields
            if not keywords or not locations:
                return JsonResponse({"error": "Keywords and locations are required parameters."}, status=400)

            print(f"Received Keywords: {keywords}, Locations: {locations}, Max Results: {max_results}, Fields: {fields}")

            # Generate queries for scraping
            queries = [f"{keyword} in {location}" for keyword in keywords for location in locations]

            # Perform scraping with Gmaps
            raw_results = Gmaps.places(
                queries,
                max=max_results,
                scrape_reviews=scrape_reviews,
                convert_to_english=convert_to_english,
                key=api_key,
                lang=lang
            )

            # Filter results based on requested fields and calculate result count
            filtered_results = []
            for query_result in raw_results:
                places = query_result.get("places", [])
                filtered_places = [
                    {field: place.get(field) for field in fields if field in place}
                    for place in places
                ]
                filtered_results.append({
                    "query": query_result.get("query"),
                    "places": filtered_places,
                    "place_count": len(filtered_places)  # Add count of places for this query
                })

            print(f"Scraping completed. Filtered Results: {filtered_results}")

            # Return results as JSON
            return JsonResponse({
                "results": filtered_results,
                "total_result_count": sum(len(query_result.get("places", [])) for query_result in raw_results)
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided."}, status=400)
        except Exception as e:
            print(f"Error in scrape_view: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)


def scrape_form(request):
    """
    Handle the rendering of the form for scraping inputs.
    """
    return render(request, "scraper_form.html")
