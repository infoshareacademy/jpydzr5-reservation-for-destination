from django.template.response import TemplateResponse


def index(request):
    menu_positions = [
        {"name": "Cennik", "url": "price_list"},
        {"name": "Repertuar", "url": "repertoire"},
        {"name": "Koszyk", "url": "basket"}
    ]
    template = "cinema/index.html"
    return TemplateResponse(request, template, {"menu_positions": menu_positions})


# Create your views here.
def basket(request):
    template = "cinema/basket.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)


def repertoire(request):
    template = "cinema/repertoire.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)


# Create your views here.
def price_list(request):
    template = "cinema/price_list.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)