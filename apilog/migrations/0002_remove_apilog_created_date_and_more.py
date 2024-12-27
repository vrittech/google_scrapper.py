# Generated by Django 5.1.4 on 2024-12-22 06:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apilog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apilog',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='apilog',
            name='updated_date',
        ),
        migrations.AddField(
            model_name='apilog',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='apilog',
            name='response_time',
            field=models.FloatField(blank=True, help_text='Response time in seconds', null=True),
        ),
        migrations.AlterField(
            model_name='apilog',
            name='data_volume',
            field=models.FloatField(help_text='Data volume in KB or MB'),
        ),
        migrations.AlterField(
            model_name='apilog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
