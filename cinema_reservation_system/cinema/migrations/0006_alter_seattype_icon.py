# Generated by Django 5.0.7 on 2024-09-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_seattype_remove_reservation_row_remove_seat_column_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seattype',
            name='icon',
            field=models.ImageField(null=True, upload_to='icons/'),
        ),
    ]
