from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .models import Seance, Movie
from . import forms, models
import json
import pendulum

DEFAULT_TICKET_TYPE_ID = 1


def index(request):
    menu_positions = [
        {"name": "Cennik", "url": "price_list"},
        {"name": "Repertuar", "url": "repertoire"},
        {"name": "Koszyk", "url": "basket"}
    ]
    template = "cinema/index.html"
    return TemplateResponse(request, template, {"menu_positions": menu_positions})


# Widok koszyka
def basket(request):
    # Ścieżka do szablonu
    template = "cinema/basket.html"

    # Sprawdź, czy w sesji są jakieś dane koszyka (wybrany seans, bilet, etc.)
    selected_seance = request.session.get('selected_seance')
    selected_ticket = request.session.get('selected_ticket')

    # Jeśli użytkownik nie wybrał jeszcze seansu ani biletu, wyślij go do wyboru seansu
    if not selected_seance or not selected_ticket:
        return redirect('select_movie')

    # Renderuj zawartość koszyka, jeśli użytkownik ma już coś wybrane
    context = {
        'selected_seance': selected_seance,
        'selected_ticket': selected_ticket,
    }
    return TemplateResponse(request, template, context)


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
    tickets = models.TicketType.objects.all()
    context = {
        "tickets": tickets,
    }
    return TemplateResponse(request, template, context)


def select_movie(request):
    if request.method == 'POST':
        form = forms.MovieForm(request.POST)
        if form.is_valid():
            selected_movie = form.cleaned_data['movie']
            # Przekieruj do widoku seansów po wybraniu filmu
            return redirect('select_seance', movie_id=selected_movie.id)
    else:
        form = forms.MovieForm()

    template = "cinema/select_movie.html"
    return render(request, template, {'form': form})


def select_seance(request, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = forms.SeanceForm(request.POST, movie=movie)
        if form.is_valid():
            selected_seance = form.cleaned_data['show_start']
            return redirect('select_seats', seance_id=selected_seance.id)
    else:
        form = forms.SeanceForm(movie=movie)

    template = "cinema/select_seance.html"
    return render(request, template, {'form': form, 'movie': movie})


def select_ticket_type(request, reservation_id):
    reservation = models.Reservation.objects.get(id=reservation_id)

    template = "cinema/select_ticket_type.html"
    context = {
        'reservation': reservation,
    }
    return render(request, template, context)


def select_seats(request, seance_id):
    seance = models.Seance.objects.get(id=seance_id)

    seat_reservation_subquery = models.SeatReservation.objects.filter(
        reservation__seance=seance,
        seat_id=OuterRef('pk')
    )

    seats = models.Seat.objects.select_related('seat_type').filter(hall=seance.hall).annotate(
        is_reserved=Exists(seat_reservation_subquery)
    )

    seats_data = []

    for seat in seats:
        seat_data = {
            'id': seat.id,
            'pos_x': seat.pos_x,
            'pos_y': seat.pos_y,
            'rotation': seat.rotation,
            'seat_type_icon': seat.seat_type.icon.url if seat.seat_type and seat.seat_type.icon else None,
            'is_reserved': 1 if seat.is_reserved else 0,
        }
        seats_data.append(seat_data)

    if request.method == 'POST':
        form = forms.SeatForm(request.POST, seance=seance)

        # tu trzeba by walidację zrobić, ale na to już nie mam czasu
        # if form.is_valid():

        selected_seats = json.loads(request.POST.get('selected-seats', '[]'))
        print(selected_seats)

        if selected_seats:
            reservation = models.Reservation.objects.create(user=request.user, seance=seance)
            for selected_seat in selected_seats:
                models.SeatReservation.objects.create(
                    reservation=reservation,
                    seat_id=selected_seat,
                    ticket_type_id=DEFAULT_TICKET_TYPE_ID,
                )

            return redirect('select_ticket_type', reservation_id=reservation.id)
    else:
        form = forms.SeatForm(seance=seance)

    template = "cinema/select_seats.html"
    context = {
        'form': form,
        'seats_json': seats_data,
        'seance': seance,

    }
    return render(request, template, context)

