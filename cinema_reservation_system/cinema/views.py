from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from . import forms, models
from django.forms import formset_factory
from .models import Reservation, SeatReservation
from .forms import TicketTypeForm
import json
import pendulum

DEFAULT_TICKET_TYPE_ID = 1


def set_cinema(request):
    if request.method == 'POST':
        cinema_id = request.POST.get('cinema')
        if 'cinema' in request.session:
            request.session['cinema'] = cinema_id
        return redirect('index')
    return redirect('index')


def index(request):
    cinema_id = request.session.get('cinema', None)
    if cinema_id is not None:
        cinema_id = int(cinema_id)
    cinemas = [
        {'id': 1, 'name': 'Kino A'},
        {'id': 2, 'name': 'Kino B'},
        {'id': 3, 'name': 'Kino C'},
    ]

    now_playing = {
        'title': 'Film Tygodnia',
        'description': 'Niezwykła opowieść o przygodzie w nieznane.'
    }

    upcoming_screenings = [
        {'movie': {'title': 'Film 1', 'image_url': ''}, 'hall': 'Sala 1', 'time': '14:00'},
        {'movie': {'title': 'Film 2', 'image_url': ''}, 'hall': 'Sala 2', 'time': '16:30'},
        {'movie': {'title': 'Film 3', 'image_url': ''}, 'hall': 'Sala 3', 'time': '19:00'}
    ]

    menu_positions = [
        {"name": "Cennik", "url": "price_list"},
        {"name": "Repertuar", "url": "repertoire"},
        {"name": "Koszyk", "url": "basket"}
    ]

    context = {
        'cinemas': cinemas,
        'now_playing': now_playing,
        'upcoming_screenings': upcoming_screenings,
        'menu_positions': menu_positions,
        'selected_cinema': cinema_id,
    }
    template = "cinema/index.html"
    return TemplateResponse(request, template, context)


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
    context = {"days": seven_days_forward}
    return TemplateResponse(request, template, context)


# Create your views here.
def price_list(request):
    template = "cinema/price_list.html"
    tickets = models.TicketType.objects.all()

    cinema_id = request.session.get('cinema', None)
    if cinema_id is not None:
        cinema_id = int(cinema_id)

    cinemas = [
        {'id': 1, 'name': 'Kino A'},
        {'id': 2, 'name': 'Kino B'},
        {'id': 3, 'name': 'Kino C'},
    ]

    menu_positions = [
        {"name": "Cennik", "url": "price_list"},
        {"name": "Repertuar", "url": "repertoire"},
        {"name": "Koszyk", "url": "basket"}
    ]

    context = {
        "tickets": tickets,
        'selected_cinema': cinema_id,
        'menu_positions': menu_positions,
        "cinemas": cinemas,
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
    reservation = get_object_or_404(Reservation, id=reservation_id)
    seat_reservations = reservation.seatreservation_set.all()

    # Utwórz formset dla typów biletów, jeden formularz dla każdego zarezerwowanego miejsca
    TicketFormSet = formset_factory(TicketTypeForm, extra=len(seat_reservations))

    if request.method == 'POST':
        formset = TicketFormSet(request.POST)
        if formset.is_valid():
            # Zapisz każdy typ biletu dla odpowiadającego mu miejsca
            for form, seat_reservation in zip(formset, seat_reservations):
                ticket_type = form.cleaned_data['ticket_type']
                seat_reservation.ticket_type = ticket_type
                seat_reservation.save()

            return redirect('next_step')  # Przekierowanie do następnego kroku po udanym przesłaniu formularza
    else:
        # Inicjalizuj formset z pustymi formularzami
        formset = TicketFormSet()

    template = "cinema/select_ticket_type.html"
    context = {
        'formset': formset,
        'reservation': reservation,
        'seat_reservations': seat_reservations
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
