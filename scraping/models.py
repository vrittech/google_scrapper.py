from django.db import models
import uuid
from django.utils.text import slugify

class ScrapedData(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField( blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name if self.name else "Unnamed"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) if self.name else str(uuid.uuid4())
            unique_slug = base_slug
            counter = 1
            while ScrapedData.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
