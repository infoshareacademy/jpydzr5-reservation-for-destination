# Generated by Django 5.0.7 on 2024-10-19 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0017_rename_collection_seatreservation_reservation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]