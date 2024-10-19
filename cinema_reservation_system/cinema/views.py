from django.db.models import Exists, OuterRef, F, ExpressionWrapper, DateTimeField
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

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
        if cinema_id:
            request.session['cinema'] = cinema_id
        else:
            request.session.pop('cinema', 'None')
        return redirect('cinema:index')
    return redirect('cinema:index')


def index(request):
    cinema_id = request.session.get('cinema', None)
    if cinema_id is not None:
        cinema_id = int(cinema_id)

    cinemas = models.Cinema.objects.values('id', 'name')
    now_playing = None
    message = "Wybierz kino, aby zobaczyć najbliższe seanse."
    upcoming_screenings = []
    current_time = pendulum.now()

    if cinema_id:
        now_playing_seance = models.Seance.objects.annotate(
            end_time=ExpressionWrapper(
                F('show_start') + F('movie__duration'), output_field=DateTimeField()
            )
        ).filter(
            hall__cinema_id=cinema_id,
            show_start__lte=current_time,
            end_time__gte=current_time
        ).select_related('movie').first()

        if now_playing_seance:
            now_playing = {
                'title': now_playing_seance.movie.title,
                'description': now_playing_seance.movie.description,
            }

        message = None

        upcoming_screenings = models.Seance.objects.filter(
            hall__cinema_id=cinema_id,
            show_start__lte=current_time,
        ).select_related('movie').order_by('show_start')[:3]

    menu_positions = [
        {"name": "Cennik", "url": "cinema:price_list"},
        {"name": "Repertuar", "url": "cinema:repertoire"},
        {"name": "Rezerwacja", "url": "cinema:select_movie"},
        {"name": "Koszyk", "url": "cinema:basket"}
    ]

    context = {
        'cinemas': cinemas,
        'now_playing': now_playing,
        'upcoming_screenings': upcoming_screenings,
        'menu_positions': menu_positions,
        'selected_cinema': cinema_id,
        'message': message
    }
    template = "cinema/index.html"
    return TemplateResponse(request, template, context)


def basket(request):
    if request.user.is_authenticated:
        # TODO: po zmianie modelu
        # seanse, które trwają już ponad 30 minut nie ma sensu utrzymywać rezerwacji
        # Reservation.objects.filter(
        #    seance__show_start__lte=pendulum.now().subtract(minutes=30)
        # ).update(status=EXPIRED)
        # seanse, które będą za mniej niż 30 minut i nie są zapłacone - kasujemy
        # Reservation.objects.filter(
        #    paid=False,
        #    seance__show_start__lte=pendulum.now().add(minutes=30)
        # ).update(status=CANCELLED)
        reservations = Reservation.objects.filter(user=request.user)
        # reservations = Reservation.objects.filter(user=request.user).exclude(status__in=[CANCELLED, EXPIRED))
    else:
        return redirect(f'{reverse("cinema:login")}?next={request.path}')

    # Jeśli użytkownik nie wybrał jeszcze seansu ani biletu, wyślij go do wyboru seansu
    if not reservations:
        return redirect('cinema:reservation')

    # Renderuj zawartość koszyka, jeśli użytkownik ma już coś wybrane
    context = {
        'reservations': reservations,
    }
    template = "cinema/basket.html"
    return TemplateResponse(request, template, context)


def repertoire(request):
    start_day = pendulum.now("Europe/Warsaw")
    seven_days_forward = {}
    for day in range(1, 8):
        start_day = start_day.add(days=1)
        seven_days_forward[start_day.format("YYYY-MM-DD")] = start_day.format("dddd", locale="pl")
    context = {"days": seven_days_forward}
    template = "cinema/repertoire.html"
    return TemplateResponse(request, template, context)


# Create your views here.
def price_list(request):
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
        {"name": "Cennik", "url": "cinema:price_list"},
        {"name": "Repertuar", "url": "cinema:repertoire"},
        {"name": "Rezerwacja", "url": "cinema:select_movie"},
        {"name": "Koszyk", "url": "cinema:basket"}
    ]

    context = {
        "tickets": tickets,
        'selected_cinema': cinema_id,
        'menu_positions': menu_positions,
        "cinemas": cinemas,
    }
    template = "cinema/price_list.html"
    return TemplateResponse(request, template, context)


def select_movie(request):
    if request.method == 'POST':
        form = forms.MovieForm(request.POST)
        if form.is_valid():
            selected_movie = form.cleaned_data['movie']
            # Przekieruj do widoku seansów po wybraniu filmu
            return redirect('cinema:select_seance', movie_id=selected_movie.id)
    else:
        form = forms.MovieForm()

    template = "cinema/select_movie.html"
    context = {
        'form': form,
    }
    return render(request, template, context)


def select_seance(request, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = forms.SeanceForm(request.POST, movie=movie)
        if form.is_valid():
            selected_seance = form.cleaned_data['show_start']
            return redirect('cinema:select_seats', seance_id=selected_seance.id)
    else:
        form = forms.SeanceForm(movie=movie)

    context = {
        'form': form,
        'movie': movie,
    }
    template = "cinema/select_seance.html"
    return render(request, "cinema/select_seance.html", context)


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

            return redirect('cinema:basket')  # Przekierowanie do następnego kroku po udanym przesłaniu formularza
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

    selected_seats = request.session.get('selected_seats', [])

    if request.method == 'POST':

        form = forms.SeatForm(request.POST, seance=seance)

        # tu trzeba by walidację zrobić, ale na to już nie mam czasu
        # if form.is_valid():

        if not request.user.is_authenticated:
            request.session['selected_seats'] = selected_seats
            # Przekierowanie na stronę logowania z parametrem `next`
            return redirect(f'{reverse("cinema:login")}?next={request.path}')
        else:
            selected_seats = json.loads(request.POST.get('selected-seats', '[]'))

        if selected_seats:
            reservation = models.Reservation.objects.create(user=request.user, seance=seance)
            for selected_seat in selected_seats:
                models.SeatReservation.objects.create(
                    reservation=reservation,
                    seat_id=selected_seat,
                    ticket_type_id=DEFAULT_TICKET_TYPE_ID,
                )

            if 'selected_seats' in request.session:
                del request.session['selected_seats']

            return redirect('cinema:select_ticket_type', reservation_id=reservation.id)
    else:
        form = forms.SeatForm(seance=seance, initial={'selected_seats': selected_seats})

    context = {
        'form': form,
        'seats_json': seats_data,
        'seance': seance,

    }
    template = "cinema/select_seats.html"
    return render(request, template, context)
