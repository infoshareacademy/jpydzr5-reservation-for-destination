from django.test import TestCase
from django.urls import reverse

class CinemaViewsTest(TestCase):

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cinema/index.html")
        self.assertIn("menu_positions", response.context)
        self.assertEqual(len(response.context["menu_positions"]), 3)

    def test_basket_view(self):
        response = self.client.get(reverse("basket"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cinema/basket.html")
        self.assertEqual(response.context["message"], "OK!")

    def test_price_list_view(self):
        response = self.client.get(reverse("price_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cinema/price_list.html")
        self.assertEqual(response.context["message"], "OK!")

    def test_repertoire_view(self):
        response = self.client.get(reverse("repertoire"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cinema/repertoire.html")
        self.assertIn("days", response.context)
        self.assertEqual(len(response.context["days"]), 7)