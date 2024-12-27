from celery import shared_task
from .models import ScrapedData

@shared_task
def save_scraped_data_task(scraped_results):
    """
    Task to save scraped data into the database.
    :param scraped_results: List of dictionaries with scraped data.
    """
    for result in scraped_results:
        try:
            ScrapedData.objects.create(
                name=result.get("name"),
                details=result.get("details"),
                phone_number=result.get("phone_number"),
                website=result.get("website"),
            )
        except Exception as e:
            print(f"Error saving data: {e}")
