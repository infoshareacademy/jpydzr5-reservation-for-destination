import os
import django
from django.conf import settings  # Importowanie settings
from django.test import TestCase
from pathlib import Path


# Ustawienie zmiennej DJANGO_SETTINGS_MODULE, aby wskazywała na Twój plik settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'cinema_reservation_system.settings'
django.setup()


class SettingsTestCase(TestCase):
    def test_secret_key(self):
        self.assertNotEqual(settings.SECRET_KEY, "django-insecure-9-ukafo0&oo39aq(v2@q*!3w$t5k(*@lvwn@^n7dm55$g@up+c")
        self.assertTrue(len(settings.SECRET_KEY) > 0)

    def test_debug(self):
        self.assertTrue(settings.DEBUG)

    def test_installed_apps(self):
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)
        self.assertIn('cinema', settings.INSTALLED_APPS)

    def test_database_settings(self):
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(settings.DATABASES['default']['NAME'], str(Path(settings.BASE_DIR) / 'db.sqlite3'))

    def test_static_url(self):
        self.assertEqual(settings.STATIC_URL, 'static/')