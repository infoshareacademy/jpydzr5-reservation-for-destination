# Generated by Django 5.0.7 on 2024-10-19 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0017_rename_collection_seatreservation_reservation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="poster",
            field=models.ImageField(blank=True, null=True, upload_to="posters/"),
        ),
    ]
