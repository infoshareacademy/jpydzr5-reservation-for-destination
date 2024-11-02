from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Exists, OuterRef, F, Q, ExpressionWrapper, DateTimeField
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from . import forms, models, decorators
from .functions import generate_qr_code, free_seats_for_seance, get_reservation_data
import json
import pendulum
from django.contrib import messages

DEFAULT_TICKET_TYPE_ID = 1
DISABLED_SEAT_TYPE_ID = 3


def qr_code_view(request, reservation_id):
    reservation = get_object_or_404(models.Reservation, pk=reservation_id)
    if not reservation.paid:
        return

    reservation_data = get_reservation_data(reservation_id)

    # Konwertuj dane na format JSON
    reservation_json = json.dumps(reservation_data)
    print(reservation_json)
    # Generowanie kodu QR
    response = generate_qr_code(reservation_json)

    return response

def set_cinema(request):
    if request.method == 'POST':
        cinema_id = request.POST.get('cinema')
        if cinema_id:
            request.session['cinema'] = cinema_id
        else:
            request.session.pop('cinema', 'None')
        return redirect('cinema:index')
    return redirect('cinema:index')


@decorators.set_vars
def index(request, context):

    now_playing = None
    message = "Wybierz kino, aby zobaczyć najbliższe seanse."
    upcoming_screenings = []
    current_time = pendulum.now()
    if 'selected_cinema' in context:
        now_playing_seance = models.Seance.objects.annotate(
            end_time=ExpressionWrapper(
                F('show_start') + F('movie__duration'), output_field=DateTimeField()
            )
        ).filter(
            hall__cinema=context['selected_cinema'],
            show_start__lte=current_time,
            end_time__gte=current_time
        ).select_related('movie').first()

        if now_playing_seance:
            now_playing = {
                'title': now_playing_seance.movie.title,
                'description': now_playing_seance.movie.description,
                'poster': now_playing_seance.movie.poster
            }

        message = None

        upcoming_screenings = models.Seance.objects.filter(
            hall__cinema=context['selected_cinema'],
            show_start__gte=current_time,
        ).select_related('movie').order_by('show_start')[:3]

    context = {
        **context,
        'now_playing': now_playing,
        'upcoming_screenings': upcoming_screenings,
        'message': message
    }
    template = "cinema/index.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def basket(request, context):
    if request.user.is_authenticated:
        reservations = models.Reservation.objects.filter(
            Q(
                paid=True
            ) | Q(
                paid=False,
                seance__show_start__gte=pendulum.now().add(minutes=30),
            ),
            user=request.user,
        )
    else:
        return redirect(f'{reverse("cinema:login")}?next={request.path}')

    # Jeśli użytkownik nie wybrał jeszcze seansu ani biletu, wyślij go do wyboru seansu
    if not reservations:
        return redirect('cinema:reservation')

    # Renderuj zawartość koszyka, jeśli użytkownik ma już coś wybrane
    context = {
        **context,
        'reservations': reservations,
    }
    template = "cinema/basket.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def repertoire(request, context):
    if 'selected_date' in request.GET:
        current_date = pendulum.parse(request.GET.get('selected_date'))
    else:
        current_date = pendulum.now()

    seances = models.Seance.objects.filter(show_start__range=(current_date, current_date.add(days=1).start_of('day')))
    date_options = [pendulum.now().add(days=i) for i in range(7)]

    # Przypisujemy filmy i seanse do słownika
    movies_with_seances = {}
    for seance in seances:
        movie = seance.movie
        seat_info = free_seats_for_seance(seance)

        if movie not in movies_with_seances:
            movies_with_seances[movie] = []

        movies_with_seances[movie].append({
            'seance': seance,
            'free_seats_count': seat_info['free_seats_count'],
            'disabled_seat_count': seat_info['free_disabled_seats_count'],
        })

    context = {
        **context,
        'current_date': current_date,
        "date_options": date_options,
        'movies': movies_with_seances,
    }
    template = "cinema/repertoire.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def price_list(request, context):
    tickets = models.TicketType.objects.all()

    cinema_id = request.session.get('cinema', None)
    if cinema_id is not None:
        cinema_id = int(cinema_id)

    context = {
        **context,
        "tickets": tickets,
    }
    template = "cinema/price_list.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def select_movie(request, context):
    if request.method == 'POST':
        form = forms.MovieForm(request.POST)
        if form.is_valid():
            selected_movie = form.cleaned_data['movie']
            # Przekieruj do widoku seansów po wybraniu filmu
            return redirect('cinema:select_seance', movie_id=selected_movie.id)
    else:
        form = forms.MovieForm()

    template = "cinema/select_movie.html"
    context = {**context,
        'form': form,
    }
    return render(request, template, context)


@decorators.set_vars
def select_seance(request, context, movie_id):
    movie = models.Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = forms.SeanceForm(request.POST, movie=movie)
        if form.is_valid():
            selected_seance = form.cleaned_data['show_start']
            return redirect('cinema:select_seats', seance_id=selected_seance.id)
    else:
        form = forms.SeanceForm(movie=movie)

    context = {
        **context,
        'form': form,
        'movie': movie,
    }
    template = "cinema/select_seance.html"
    return render(request, template, context)


@decorators.set_vars
def select_ticket_type(request, context, reservation_id):
    reservation = get_object_or_404(models.Reservation, id=reservation_id)
    seat_reservations = reservation.seatreservation_set.all()

    # Utwórz formset dla typów biletów, jeden formularz dla każdego zarezerwowanego miejsca
    TicketFormSet = formset_factory(forms.TicketTypeForm, extra=len(seat_reservations))

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
        **context,
        'formset': formset,
        'reservation': reservation,
        'seat_reservations': seat_reservations
    }
    return render(request, template, context)


@decorators.set_vars
@login_required
def select_seats(request, context, seance_id):
    seance = get_object_or_404(models.Seance, id=seance_id)

    # Zapytanie do bazy danych o zarezerwowane miejsca
    seat_reservation_subquery = models.SeatReservation.objects.filter(
        reservation__seance=seance,
        seat_id=OuterRef('pk')
    )

    seats = models.Seat.objects.select_related('seat_type').filter(hall=seance.hall).annotate(
        is_reserved=Exists(seat_reservation_subquery)
    )

    seats_data = [
        {
            'id': seat.id,
            'pos_x': seat.pos_x,
            'pos_y': seat.pos_y,
            'rotation': seat.rotation,
            'seat_type_icon': seat.seat_type.icon.url if seat.seat_type and seat.seat_type.icon else None,
            'is_reserved': 1 if seat.is_reserved else 0,
        } for seat in seats
    ]

    if request.method == 'POST':
        selected_seats = {int(x) for x in json.loads(request.POST.get('selected-seats', '[]'))}
        if selected_seats:
            # Walidacja dostępnych miejsc
            available_seats = {seat.id for seat in seats}
            if not selected_seats.issubset(available_seats):  # zbiór pierwszy wykracza poza zbiór drugi
                messages.error(request, "Niektóre miejsca nie są dostępne.")
                return redirect('cinema:select_seats', seance_id=seance_id)

            # Tworzenie rezerwacji
            reservation = models.Reservation.objects.create(user=request.user, seance=seance)
            for selected_seat in selected_seats:
                models.SeatReservation.objects.create(
                    reservation=reservation,
                    seat_id=selected_seat,
                    ticket_type_id=DEFAULT_TICKET_TYPE_ID,
                )
            return redirect('cinema:select_ticket_type', reservation_id=reservation.id)

    context.update({
        'seats_json': seats_data,
        'seance': seance,
    })
    return render(request, "cinema/select_seats.html", context)

@login_required
@decorators.set_vars
def user_panel_view(request, context):
    user = request.user  # Pobiera zalogowanego użytkownika
    # Możesz pobierać dodatkowe dane, np. historię rezerwacji
    context = {
        **context,
        'user': user,
        # Możesz dodać tutaj inne dane związane z użytkownikiem
    }
    template = 'cinema/user_panel.html'
    return render(request, template, context)


@login_required
@decorators.set_vars
def edit_user_panel_view(request, context):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('cinema:user_panel')  # Po zapisaniu przekierowanie do panelu użytkownika
    else:
        form = UserChangeForm(instance=request.user)
    template = 'cinema/edit_user_panel.html'
    context = {
        **context,
        'form': form,
    }
    return render(request, template, context)
