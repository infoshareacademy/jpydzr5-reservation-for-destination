import os
import django


os.environ['DJANGO_SETTINGS_MODULE'] = "cinema_reservation_system.settings"
django.setup()

from django.test import TestCase
from django.urls import reverse, resolve

# Reszta kodu testu


from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

class UrlsTestCase(TestCase):
    def test_main_page_redirect(self):
        response = self.client.get(reverse('main_page'))
        self.assertRedirects(response, 'cinema/', status_code=302)

    def test_cinema_url_resolves(self):
        resolver = resolve('cinema/')
        self.assertEqual(resolver.view_name, 'index')

    def test_admin_url_resolves(self):
        resolver = resolve('admin/')
        self.assertEqual(resolver.func.__name__, 'index')