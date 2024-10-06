from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractMinute, ExtractWeekDay
from django.http import HttpResponse
from django.shortcuts import render

from cinema import models
import pendulum

DAYS_OF_WEEK = {
    1: "Niedziela",
    2: "Poniedziałek",
    3: "Wtorek",
    4: "Środa",
    5: "Czwartek",
    6: "Piątek",
    7: "Sobota",
}

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
    popular_showtimes = (
        models.SeatReservation.objects.annotate(
            hour=ExtractHour('reservation__seance__show_start'),
            minute=ExtractMinute('reservation__seance__show_start')
        ).exclude(hour__isnull=True)
        .values('hour','minute')  # Grupuje po godzinie
        .annotate(count=Count('id'))  # Zlicza wystąpienia seansów dla każdej godziny
        .order_by('-count')  # Sortuje według liczby wystąpień malejąco
    )
    popular_weekdays = (
        models.SeatReservation.objects.annotate(weekday=ExtractWeekDay('reservation__seance__show_start'))  # Ekstrahuje godzinę
        .exclude(weekday__isnull=True)
        .values('weekday')
        .annotate(count=Count('id'))  # Zlicza wystąpienia seansów dla każdej godziny
        .order_by('-count')  # Sortuje według liczby wystąpień malejąco
    )
    popular_weekdays = [
        {
            'weekday': popular_weekday['weekday'],
            'day_name': DAYS_OF_WEEK.get(popular_weekday['weekday'], "Nieznany dzień"),
            'count': popular_weekday['count']
        }
        for popular_weekday in popular_weekdays
    ]

    popular_ticket_types = (
        models.SeatReservation.objects
        .values('ticket_type', 'ticket_type__name')
        .annotate(count=Count('id'))  # Zlicza wystąpienia seansów dla każdej godziny
        .order_by('-count')  # Sortuje według liczby wystąpień malejąco
    )

    context = {
        'range_begin' : range_begin,
        'range_end': range_end,
        'popular_showtimes': popular_showtimes,
        'popular_weekdays': popular_weekdays,
        'popular_ticket_types': popular_ticket_types,
        'movies_with_reservations': movies_with_reservations,
    }
    return render(request, 'backoffice/report.html', context)

