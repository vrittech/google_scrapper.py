from django.db import models
from accounts.models import CustomUser

# Create your models here.
class APILog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    data_volume = models.FloatField(help_text="Data volume in KB or MB")
    response_time = models.FloatField(help_text="Response time in seconds", null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.endpoint}"
