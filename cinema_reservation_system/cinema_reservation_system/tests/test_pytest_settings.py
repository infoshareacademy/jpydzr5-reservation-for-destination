import os
import django
import pytest

from cinema_reservation_system import settings

# Ustawienie zmiennej DJANGO_SETTINGS_MODULE, aby wskazywała na plik settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'cinema_reservation_system.settings'
django.setup()


@pytest.fixture(scope='module', autouse=True)
def setup_django():
    """Fixture odpowiedzialny za wstępne ustawienie Django."""
    django.setup()


def test_database_settings():
    """Sprawdza, czy domyślny silnik bazy danych to SQLite."""
    assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3'