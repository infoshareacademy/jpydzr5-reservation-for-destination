# Generated by Django 5.0.6 on 2024-09-08 11:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
    ]
