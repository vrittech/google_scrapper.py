# Generated by Django 5.1.4 on 2024-12-22 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('Success', 'Success'), ('Failed', 'Failed')], default='Success', max_length=20),
        ),
    ]
