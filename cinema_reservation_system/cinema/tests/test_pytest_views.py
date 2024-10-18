import os
import pytest
from django.urls import reverse
from django.test import Client

@pytest.fixture(scope="module", autouse=True)
def setup_django_environment():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cinema_reservation_system.settings'
    import django
    django.setup()

@pytest.fixture
def client():
    return Client()

def test_index_view(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200
    assert "cinema/index.html" in [t.name for t in response.templates]
    assert "menu_positions" in response.context
    assert len(response.context["menu_positions"]) == 3

def test_basket_view(client):
    response = client.get(reverse("basket"))
    assert response.status_code == 200
    assert "cinema/basket.html" in [t.name for t in response.templates]
    assert response.context["message"] == "OK!"

def test_price_list_view(client):
    response = client.get(reverse("price_list"))
    assert response.status_code == 200
    assert "cinema/price_list.html" in [t.name for t in response.templates]
    assert response.context["message"] == "OK!"

def test_repertoire_view(client):
    response = client.get(reverse("repertoire"))
    assert response.status_code == 200
    assert "cinema/repertoire.html" in [t.name for t in response.templates]
    assert "days" in response.context
    assert len(response.context["days"]) == 7