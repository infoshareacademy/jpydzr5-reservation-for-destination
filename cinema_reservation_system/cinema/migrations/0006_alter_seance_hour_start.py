# Generated by Django 5.0.6 on 2024-08-28 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_alter_seance_hall_number_alter_seance_hour_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='hour_start',
            field=models.TimeField(max_length=4),
        ),
    ]
