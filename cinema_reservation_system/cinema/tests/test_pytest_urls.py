import pytest
from django.urls import resolve, reverse
from .. import views

@pytest.mark.parametrize("url_name, view_func", [
    ('index', views.index),
    ('price_list', views.price_list),
    ('repertoire', views.repertoire),
    ('basket', views.basket),
])
def test_url_resolves(url_name, view_func):
    """Testuje, czy URL jest poprawnie przypisany do widoku."""
    url = reverse(url_name)
    assert resolve(url).func == view_func