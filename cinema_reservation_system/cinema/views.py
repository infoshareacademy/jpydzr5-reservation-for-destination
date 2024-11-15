from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.db import transaction
from django.db.models import Exists, OuterRef, F, Q, ExpressionWrapper, DateTimeField, Sum, Count
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from . import forms, models, decorators
import json
import pendulum
from django.contrib import messages
from .functions import free_seats_for_seance, get_reservation_data
from .forms import UserEditForm, CustomUserChangeForm, generate_seat_ticket_forms
from .models import Reservation

DEFAULT_TICKET_TYPE_ID = 1
DISABLED_SEAT_TYPE_ID = 3


@login_required
def user_panel(request):
    return render(request, 'cinema/user_panel.html', {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    })


@login_required
def edit_user_panel(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dane zostały pomyślnie zaktualizowane.')
            return redirect('cinema:user_panel')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'cinema/edit_user_panel.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Twoje hasło zostało zmienione.')
            return redirect('cinema:user_panel')
        else:
            messages.error(request, 'Wystąpił błąd przy zmianie hasła.')
    return redirect('cinema:user_panel')


def set_cinema(request):
    if request.method == 'POST':
        selected_cinema_id = request.POST.get('selected_cinema_id')
        if selected_cinema_id:
            request.session['selected_cinema_id'] = selected_cinema_id
        else:
            request.session.pop('selected_cinema_id', 'None')

        next_url = request.POST.get("next", reverse("cinema:index"))
        return redirect(next_url)
    return redirect('cinema:index')


@decorators.set_vars
def index(request, context):

    message = ""
    upcoming_screenings = []
    current_time = pendulum.now().subtract(minutes=30)
    if 'selected_cinema' in context:
        seances = models.Seance.objects.filter(
            hall__cinema=context['selected_cinema'],
            show_start__gte=current_time,
        ).order_by('show_start')
        # tu powinien być distinct, ale nie działa na sqlite

        upcoming_screenings = {}
        count = 3
        for seance in seances:
            movie = seance.movie
            seat_info = free_seats_for_seance(seance)
            if movie not in upcoming_screenings:
                upcoming_screenings[movie] = {
                    'seance': seance,
                    'free_seats_count': seat_info['free_seats_count'],
                    'disabled_seat_count': seat_info['free_disabled_seats_count'],
                }
                count -= 1
            if count == 0:
                break
    else:
        message = "Wybierz kino, aby zobaczyć najbliższe seanse."
    context.update({
        'upcoming_screenings': upcoming_screenings,
        'message': message
    })
    template = "cinema/index.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def tickets(request, context):
    if request.user.is_authenticated:
        reservations = models.Reservation.objects.annotate(
            seat_count=Count('seatreservation')
        ).filter(
            paid=True,
            user=request.user,
            seat_count__gt=0,
        )
        if 'selected_cinema' in context:
            reservations = reservations.filter(
                seance__hall__cinema=context['selected_cinema'],
            )
    else:
        return redirect(f'{reverse("cinema:login")}?next={request.path}')

    # Jeśli użytkownik nie wybrał jeszcze seansu ani biletu, wyślij go do wyboru seansu
    #if not reservations:
    #    return redirect('cinema:repertoire')

    # Renderuj zawartość koszyka, jeśli użytkownik ma już coś wybrane
    context.update({
        'reservations': reservations,
    })
    template = "cinema/tickets.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def basket(request, context):
    if request.user.is_authenticated:
        # Pobierz rezerwacje użytkownika, które nie zostały opłacone
        reservations = models.Reservation.objects.annotate(
            seat_count=Count('seatreservation')
        ).filter(
            paid=False,
            seance__show_start__gte=pendulum.now().add(minutes=30),
            user=request.user,
            seat_count__gt=0,
        )

        # Jeśli użytkownik wybrał kino, filtruj rezerwacje po kinie
        if 'selected_cinema' in context:
            reservations = reservations.filter(
                seance__hall__cinema=context['selected_cinema'],
            )

        # Oblicz całkowity koszt każdej rezerwacji
        for reservation in reservations:
            total_cost = 0
            for seat_reservation in reservation.seatreservation_set.all():
                # Jeśli cena biletu jest None, przypisz 0
                price = seat_reservation.price if seat_reservation.price is not None else 0
                total_cost += price  # Sumowanie ceny biletów
            reservation.total_cost = total_cost  # Dodanie do obiektu rezerwacji

    else:
        return redirect(f'{reverse("cinema:login")}?next={request.path}')

    # Jeśli użytkownik nie ma rezerwacji, przekieruj do repertuaru
    # if not reservations:
    #     return redirect('cinema:repertoire')

    # Przekazanie rezerwacji oraz ich całkowitych kosztów do kontekstu
    context.update({
        'reservations': reservations,
        'total_cost': sum(reservation.total_cost for reservation in reservations),  # Sumaryczny koszt wszystkich rezerwacji
    })

    # Renderowanie szablonu koszyka
    template = "cinema/basket.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def repertoire(request, context):
    if 'selected_cinema' not in context:
        return redirect(f'{reverse("cinema:index")}')

    if 'selected_date' in request.GET:
        current_time = pendulum.parse(request.GET.get('selected_date'))
    else:
        current_time = pendulum.now()
    if current_time < pendulum.now():
        current_time = pendulum.now().subtract(minutes=30)

    seances = models.Seance.objects.filter(
        hall__cinema=context['selected_cinema'],
        show_start__range=(current_time, current_time.add(days=1).start_of('day'))
    ).order_by('show_start')

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

    context.update({
        'current_time': current_time,
        "date_options": date_options,
        'movies': movies_with_seances,
    })
    template = "cinema/repertoire.html"
    return TemplateResponse(request, template, context)


@decorators.set_vars
def pricing(request, context):
    tickets = models.TicketType.objects.all()

    cinema_id = request.session.get('cinema_id', None)
    if cinema_id is not None:
        cinema_id = int(cinema_id)

    context.update({
        "tickets": tickets,
    })
    template = "cinema/pricing.html"
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
    context.update({
        'form': form,
    })
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

    context.update({
        'form': form,
        'movie': movie,
    })
    template = "cinema/select_seance.html"
    return render(request, template, context)


@decorators.set_vars
def select_ticket_type(request, context):
    if 'selected_seat_ids' not in request.session:
        return redirect('cinema:basket')

    selected_seance = models.Seance.objects.get(id=request.session['selected_seance_id'])
    selected_seats = models.Seat.objects.filter(id__in=set(request.session['selected_seat_ids']))

    formset = generate_seat_ticket_forms(selected_seats)

    if request.method == 'POST':
        formset = [
            forms.SeatTicketTypeForm(request.POST, seat=seat, prefix=f'seat_{seat.id}') for seat in selected_seats
        ]
        all_valid = all(form.is_valid() for form in formset)

        if all_valid:
            reservation = models.Reservation.objects.create(
                user=request.user,
                seance_id=request.session['selected_seance_id']
            )

            # Zapisz każdy typ biletu dla odpowiadającego mu miejsca
            for form in formset:
                ticket_type = form.cleaned_data['ticket_type']
                seat = form.cleaned_data['seat']
                models.SeatReservation.objects.create(
                    reservation=reservation,
                    seat=seat,
                    ticket_type=ticket_type,
                )

            del request.session['selected_seance_id']
            del request.session['selected_seat_ids']
            return redirect('cinema:basket')  # Przekierowanie do następnego kroku po udanym przesłaniu formularza

    form_with_seat = [(form, seat) for form, seat in zip(formset, selected_seats)]
    template = "cinema/select_ticket_type.html"
    context.update({
        'formset': formset,
        'form_with_seat': form_with_seat,
        'selected_seance': selected_seance,
        'selected_seats': selected_seats,
    })
    return render(request, template, context)


@decorators.set_vars
def select_seats(request, context, seance_id):
    seance = get_object_or_404(models.Seance, id=seance_id)

    selected_seats = {}
    # jeżeli była w tej sesji rezerwacja na ten seans to przywracamy, a jeśli nie na ten seans,
    # to uznajemy, że porzuca tamta rezerwację

    if 'selected_seat_ids' in request.session:
        if request.session['selected_seance_id'] != seance_id:
            del request.session['selected_seat_ids']
            request.session['selected_seance_id'] = seance_id
        else:
            selected_seats = set(request.session['selected_seat_ids'])

    seat_reservation_subquery = models.SeatReservation.objects.filter(
        reservation__seance=seance,
        seat_id=OuterRef('pk'),
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
            'is_selected': 1 if seat.id in selected_seats else 0,
        } for seat in seats
    ]

    if request.method == 'POST':
        selected_seats = {int(x) for x in json.loads(request.POST.get('selected-seats', '[]'))}
        # Walidacja dostępnych miejsc
        available_seats = {seat.id for seat in seats}
        if not selected_seats.issubset(available_seats):  # zbiór pierwszy wykracza poza zbiór drugi
            messages.error(request, "Niektóre miejsca nie są dostępne.")
            return redirect('cinema:select_seats', seance_id=seance_id)

        request.session['selected_seat_ids'] = list(selected_seats)
        request.session['selected_seance_id'] = seance_id

        if not request.user.is_authenticated:
            login_url = f"{reverse('cinema:login')}?next={request.path}"
            return redirect(login_url)

        # Tworzenie rezerwacji
        return redirect('cinema:select_ticket_type')

    context.update({
        'seats_json': seats_data,
        'seance': seance,
    })
    return render(request, "cinema/select_seats.html", context)


@login_required
@decorators.set_vars
def payment(request, context, reservation_id=None):
    if reservation_id:
        total_price = models.SeatReservation.objects.filter(
            reservation_id=reservation_id,
            reservation__user=request.user,
            reservation__seance__hall__cinema=context['selected_cinema']
        ).aggregate(
            total_price=Sum('ticket_type__price')
        )['total_price']
    else:
        total_price = models.SeatReservation.objects.filter(
            reservation__user=request.user,
            reservation__seance__hall__cinema=context['selected_cinema'],
            reservation__paid=False,
            reservation__seance__show_start__gte=pendulum.now().add(minutes=30)

        ).aggregate(
            total_price=Sum('ticket_type__price')
        )['total_price']

    if request.method == 'POST':
        if 'confirm' in request.POST:  # Jeśli użytkownik kliknął "Tak"
            if reservation_id:
                models.Reservation.objects.filter(
                    user=request.user,
                    seance__hall__cinema=context['selected_cinema'],
                    pk=reservation_id
                ).update(paid=True)
            else:
                models.Reservation.objects.filter(
                    user=request.user,
                    seance__hall__cinema=context['selected_cinema'],
                ).update(paid=True)



        return redirect('cinema:basket')

    template = 'cinema/payment.html'
    context.update(
        {"total_price": total_price}
    )
    return render(request, template, context)


@login_required
@decorators.set_vars
def user_panel_view(request, context):
    user = request.user  # Pobiera zalogowanego użytkownika
    # Możesz pobierać dodatkowe dane, np. historię rezerwacji
    context.update({
        'user': user,
        # Możesz dodać tutaj inne dane związane z użytkownikiem
    })
    template = 'cinema/user_panel.html'
    return render(request, template, context)


@login_required
def edit_user_panel_view(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()  # Zapisz dane użytkownika
            password_form.save()  # Zapisz nowe hasło
            update_session_auth_hash(request, password_form.user)  # Zaktualizuj sesję użytkownika
            messages.success(request, "Dane oraz hasło zostały pomyślnie zaktualizowane.")
            return redirect('cinema:user_panel')
        else:
            messages.error(request, "Proszę poprawić błędy w formularzu.")
    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'cinema/edit_user_panel.html', context)


def basket_view(request):
    reservation = Reservation.objects.get(user=request.user, paid=False, cancelled=False)

    # Jeśli nie ma rezerwacji, przekierowanie do strony błędu lub pustego koszyka
    if not reservation:
        return render(request, 'basket_empty.html')

    # Całkowita cena rezerwacji
    total_price = reservation.total_price

    return render(request, 'basket.html', {'reservation': reservation, 'total_price': total_price})

