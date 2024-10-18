import pytest
import os
import django
from django.core.management import call_command
from django.db import transaction, connections

@pytest.fixture(scope='module', autouse=True)
def setup_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
    django.setup()

def test_migration():
    # Specyficzne ustawienie dla SQLite, aby obejść problemy z transakcjami
    if connections['default'].vendor == 'sqlite':
        with transaction.atomic():
            connections['default'].disable_constraint_checking()
            call_command('migrate')
    else:
        call_command('migrate')