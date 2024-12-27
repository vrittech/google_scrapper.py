from celery import shared_task
from .models import WebScrapingTask
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def save_web_scraping_result(task_id, scraped_data):
    """
    Celery task to save web scraping results in the WebScrapingTask model.

    :param task_id: ID of the WebScrapingTask instance.
    :param scraped_data: Scraped data to save (JSON serializable).
    """
    try:
        # Fetch the task instance
        task = WebScrapingTask.objects.get(id=task_id)
        logger.info(f"Saving results for WebScrapingTask ID: {task_id}")

        # Update the task status to "In Progress"
        task.status = "In Progress"
        task.save(update_fields=["status", "updated_at"])

        # Serialize and save the scraped data
        task.result_data = json.dumps(scraped_data, indent=4)
        task.status = "Completed"
        task.save(update_fields=["result_data", "status", "updated_at"])

        logger.info(f"WebScrapingTask ID: {task_id} marked as Completed.")

    except WebScrapingTask.DoesNotExist:
        logger.error(f"WebScrapingTask with ID {task_id} does not exist.")
    except Exception as e:
        # Log and handle errors, marking the task as Failed
        logger.error(f"Error saving results for WebScrapingTask ID: {task_id}: {e}")
        try:
            task = WebScrapingTask.objects.get(id=task_id)
            task.status = "Failed"
            task.result_data = json.dumps({"error": str(e)}, indent=4)
            task.save(update_fields=["result_data", "status", "updated_at"])
        except WebScrapingTask.DoesNotExist:
            logger.error(f"Failed to update non-existent WebScrapingTask ID: {task_id}")
