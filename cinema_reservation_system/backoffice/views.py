from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from cinema import models
import pendulum


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the backoffice index.")


def pdf_report(request):
    return HttpResponse("Hello, world. You're at the backoffice index.")


def html_report(request):
    #     Stworzenie statystyki pod:
    #
    # Najczęściej wybierany film przez klienta (raport tyd/mięs)
    # Najczęściej wybierana godzina seansu przez klienta
    # Najczęściej wybierany dzień tygodnia przez klienta
    # Najczęściej wybierany rodzaj biletu przez klienta
    today = pendulum.today()
    range_end = today.add(days=1)
    range_begin = today.subtract(days=7)

    movies_with_reservations = (
        models.Movie.objects.filter(
            seance__show_start__gte=range_begin,
            seance__show_start__lte=range_end,
        ).annotate(
            total_reserved_seats=Count('seance__reservation__seatreservation')
        ).order_by('-total_reserved_seats')
    )
    context = {
        'movies_with_reservations': movies_with_reservations,
    }
    return render(request, 'backoffice/report.html', context)

