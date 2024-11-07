# Generated by Django 5.0.7 on 2024-11-02 23:04

import django.db.models.deletion
import pendulum
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0019_merge_20241020_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
