from django.test import TestCase
from django.apps import apps
from ..apps import CinemaConfig

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
django.setup()

class CinemaConfigTest(TestCase):

    def test_app_config(self):
        app_config = apps.get_app_config('cinema')
        self.assertEqual(app_config.name, 'cinema')
        self.assertIsInstance(app_config, CinemaConfig)

    def test_default_auto_field(self):
        app_config = apps.get_app_config('cinema')
        self.assertEqual(app_config.default_auto_field, 'django.db.models.BigAutoField')