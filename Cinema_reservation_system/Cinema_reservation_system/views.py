from django.template.response import TemplateResponse
from django.http import HttpResponse
from .forms import ChooseOptionMenuForm


def index(request):
    menu_positions = ["Cennik", "Repertuar", "Koszyk", "Zakończ program"]
    template = "index/index.html"
    form = ChooseOptionMenuForm()
    if request.method == "POST":
        form = ChooseOptionMenuForm(request.POST)
        if form.is_valid():
            return HttpResponse("OK")
    else:
        form = ChooseOptionMenuForm()
    return TemplateResponse(request, template, {"menu_positions": menu_positions, "form": form})

