# Generated by Django 5.1.4 on 2024-12-20 11:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebScrapingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_url', models.URLField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('result_data', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scraping_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]