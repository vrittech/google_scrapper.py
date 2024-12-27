# Generated by Django 5.1.4 on 2024-12-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='channel',
            field=models.CharField(choices=[('Email', 'Email'), ('SMS', 'SMS'), ('In-App', 'In-App')], default='In-App', max_length=20),
        ),
    ]