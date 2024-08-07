from django.template.response import TemplateResponse
from django.http import HttpResponse


def index(request):
    menu_positions = [
        {"name": "Cennik", "url": "cennik"},
        {"name": "Repertuar", "url": "repertuar"},
        {"name": "Koszyk", "url": "koszyk"}
    ]
    template = "index/index.html"
    return TemplateResponse(request, template, {"menu_positions": menu_positions})

