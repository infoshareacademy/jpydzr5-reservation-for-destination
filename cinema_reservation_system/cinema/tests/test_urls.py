from django.test import SimpleTestCase
from django.urls import resolve, reverse
from cinema import views

class UrlsTestCase(SimpleTestCase):

    def test_index_url_resolves(self):
        """Testuje, czy URL dla strony głównej (index) jest poprawnie przypisany do widoku."""
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_price_list_url_resolves(self):
        """Testuje, czy URL dla strony cennika (price_list) jest poprawnie przypisany do widoku."""
        url = reverse('price_list')
        self.assertEqual(resolve(url).func, views.price_list)

    def test_repertoire_url_resolves(self):
        """Testuje, czy URL dla strony repertuaru (repertoire) jest poprawnie przypisany do widoku."""
        url = reverse('repertoire')
        self.assertEqual(resolve(url).func, views.repertoire)

    def test_basket_url_resolves(self):
        """Testuje, czy URL dla strony koszyka (basket) jest poprawnie przypisany do widoku."""
        url = reverse('basket')
        self.assertEqual(resolve(url).func, views.basket)