import pytest
from django.apps import apps
from ..apps import CinemaConfig

@pytest.fixture(scope='module', autouse=True)
def setup_django():
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
    django.setup()

def test_app_config():
    app_config = apps.get_app_config('cinema')
    assert app_config.name == 'cinema'
    assert isinstance(app_config, CinemaConfig)

def test_default_auto_field():
    app_config = apps.get_app_config('cinema')
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'