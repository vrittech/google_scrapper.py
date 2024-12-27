from django.db import models
from accounts.models import CustomUser
from subscriptionplan.models import SubscriptionPlan

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending')],
        default='Pending'
    )
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.payment_status}"
