# Generated by Django 5.1.4 on 2024-12-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_api_key_customuser_api_limit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_status',
            field=models.CharField(choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Canceled', 'Canceled')], default='Active', max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='plan_renewal_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]