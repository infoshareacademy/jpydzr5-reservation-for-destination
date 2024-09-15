# Generated by Django 5.0.7 on 2024-09-14 21:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0011_reservationcollection_reservation_paid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='user',
        ),
        migrations.AddField(
            model_name='reservationcollection',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]