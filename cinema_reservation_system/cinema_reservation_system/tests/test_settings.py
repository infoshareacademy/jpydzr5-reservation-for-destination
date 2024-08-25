import os
import django
from django.test import TestCase

# Ustawienie zmiennej DJANGO_SETTINGS_MODULE, aby wskazywała na Twój plik settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'cinema_reservation_system.settings'
django.setup()


class SettingsTestCase(TestCase):

    def test_database_settings(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
