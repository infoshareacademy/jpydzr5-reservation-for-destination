# Generated by Django 5.0.7 on 2024-11-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0024_rename_hall_number_hall_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatreservation',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
