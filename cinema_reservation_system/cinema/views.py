from django.template.response import TemplateResponse

from .models import Movie, Seance
import pendulum


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
    start_day = pendulum.now("Europe/Warsaw")
    seven_days_forward = {}
    for day in range(1, 8):
        start_day = start_day.add(days=1)
        seven_days_forward[start_day.format("YYYY-MM-DD")] = start_day.format("dddd", locale="pl")
    day = request.GET.get("date")
    if day is not None:
        ids_movies = Seance.objects.filter(show_start__date=day).values_list("movie__id", flat=True).distinct()
    else:
        ids_movies = (Seance.objects.filter(show_start=pendulum.now("Europe/Warsaw").format("YYYY-MM-DD"))
                      .values_list("movie__id", flat=True)).distinct()
    movies = Movie.objects.filter(id__in=ids_movies)
    time_movies = Seance.objects.filter(movie__in=ids_movies, show_start__date=day).values_list("show_start", flat=True)
    context = {
        "days": seven_days_forward,
        "movies": movies,
        "time_movies": time_movies
    }
    return TemplateResponse(request, template, context)


# Create your views here.
def price_list(request):
    template = "cinema/price_list.html"
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)