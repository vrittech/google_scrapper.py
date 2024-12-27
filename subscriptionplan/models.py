from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discounted price for the plan."
    )
    api_limit = models.IntegerField(help_text="Maximum API calls allowed per month.")
    data_limit = models.FloatField(default=100.0, help_text="Data volume limit (in MB).")
    concurrent_scrapes = models.IntegerField(default=1, help_text="Number of concurrent scraping tasks allowed.")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    trial_days = models.IntegerField(default=0, help_text="Number of trial days (0 for no trial).")
    premium_templates = models.BooleanField(default=False, help_text="Access to premium templates.")
    dedicated_proxies = models.BooleanField(default=False, help_text="Access to dedicated proxy pools.")
    duration = models.CharField(
        max_length=20,
        choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')],
        default='Monthly',
        help_text="Subscription duration."
    )
    priority = models.IntegerField(default=0, help_text="Priority for sorting plans.")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
