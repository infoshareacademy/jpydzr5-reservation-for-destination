import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
django.setup()

from django.test import TestCase
from django.core.management import call_command
from django.db import transaction, connections

class MigrationTest(TestCase):

    def test_migration(self):
        # Specyficzne ustawienie dla SQLite, aby obejść problemy z transakcjami
        if connections['default'].vendor == 'sqlite':
            with transaction.atomic():
                connections['default'].disable_constraint_checking()
                call_command('migrate')
        else:
            call_command('migrate')

