# Generated by Django 5.0.7 on 2024-11-11 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0023_tickettype_extra_validation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hall',
            old_name='hall_number',
            new_name='name',
        ),
    ]
