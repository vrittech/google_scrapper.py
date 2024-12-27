from django.db import models
from accounts.models import CustomUser

# Create your models here.
class WebScrapingTask(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="scraping_tasks")
    target_url = models.URLField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    result_data = models.TextField(null=True, blank=True)  # JSON or CSV data as string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.target_url} - {self.status}"
