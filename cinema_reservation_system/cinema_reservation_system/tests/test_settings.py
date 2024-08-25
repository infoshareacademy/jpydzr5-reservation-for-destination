import os
import django
from django.test import TestCase
import secrets
print(secrets.token_urlsafe(50))

# Ustawienie zmiennej DJANGO_SETTINGS_MODULE, aby wskazywała na Twój plik settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'cinema_reservation_system.settings'
django.setup()

from django.conf import settings
from pathlib import Path


class SettingsTestCase(TestCase):

    def test_database_settings(self):
        # Sprawdź, czy silnik bazy danych to SQLite
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        #
        # # Sprawdź, czy ścieżka do bazy danych jest poprawna
        # expected_db_path = str(Path(settings.BASE_DIR) / 'test.db.sqlite3')
        # actual_db_path = str(Path(settings.DATABASES['default']['NAME']))  # Konwertuj do str
        # self.assertEqual(actual_db_path, expected_db_path)

    def test_secret_key(self):
        # Sprawdź, czy klucz tajny nie jest domyślnym kluczem
        self.assertNotEqual(settings.SECRET_KEY, "django-insecure-9-ukafo0&oo39aq(v2@q*!3w$t5k(*@lvwn@^n7dm55$g@up+c")