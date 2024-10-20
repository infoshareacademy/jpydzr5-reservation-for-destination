import os
import django
import pytest
from django.urls import reverse, resolve
from django.test import Client

# Ustawienie zmiennej DJANGO_SETTINGS_MODULE, aby wskazywała na plik settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
django.setup()

@pytest.fixture
def client():
    """Fixture zwracający instancję klienta testowego Django."""
    return Client()


def test_main_page_redirect(client):
    """Test sprawdzający przekierowanie z URL 'main_page'."""
    response = client.get(reverse('main_page'))
    assert response.status_code == 302
    assert response.url == '/cinema/'


def test_cinema_url_resolves():
    """Test sprawdzający poprawność przypisania URL '/cinema/' do widoku."""
    resolver = resolve('/cinema/')
    assert resolver.view_name == 'index'


def test_admin_url_resolves():
    """Test sprawdzający poprawność przypisania URL '/admin/' do widoku admina."""
    resolver = resolve('/admin/')
    assert resolver.func.__name__ == 'index'