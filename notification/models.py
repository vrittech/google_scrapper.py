from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    channel = models.CharField(
        max_length=20,
        choices=[('Email', 'Email'), ('SMS', 'SMS'), ('In-App', 'In-App')],
        default='In-App'
    )

    def __str__(self):
        return f"{self.user.username} - {self.channel} - {'Read' if self.read else 'Unread'}"
