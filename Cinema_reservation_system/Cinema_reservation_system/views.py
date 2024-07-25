from django.template.response import TemplateResponse
from django.http import HttpResponse


def index(request):
    menu_positions = [
        {"name": "Cennik", "url": "price_list"},
        {"name": "Repertuar", "url": "repertoire"},
        {"name": "Koszyk", "url": "basket"}
    ]
    template = "index/index.html"
    return TemplateResponse(request, template, {"menu_positions": menu_positions})

