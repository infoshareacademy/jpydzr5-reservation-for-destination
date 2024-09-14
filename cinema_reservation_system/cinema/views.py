from django.template.response import TemplateResponse
import pendulum
from django.shortcuts import render, redirect
from .forms import SeanceForm, TicketTypeForm, MovieForm
from .models import TicketType, Movie, Seance, Seat


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
    context = {"days": seven_days_forward}
    day = request.GET.get("date")
    return TemplateResponse(request, template, context)


# Create your views here.
def price_list(request):
    template = "cinema/price_list.html"
    tickets = TicketType.objects.all()
    context = {
        "tickets": tickets,
    }
    return TemplateResponse(request, template, context)


def select_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            selected_movie = form.cleaned_data['movie']
            # Przekieruj do widoku seansów po wybraniu filmu
            return redirect('select_seance', movie_id=selected_movie.id)
    else:
        form = MovieForm()

    template = "cinema/select_movie.html"
    return render(request, template, {'form': form})


def select_seance(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = SeanceForm(request.POST, movie=movie)
        if form.is_valid():
            selected_seance = form.cleaned_data['show_start']
            return redirect('select_seat', seance_id = selected_seance.id)
    else:
        form = SeanceForm(movie=movie)

    template = "cinema/select_seance.html"
    return render(request, template, {'form': form, 'movie': movie})


def select_seat(request, seance_id):
    seance = Seance.objects.get(id=seance_id)
    if request.method == 'POST':
        form = SeanceForm(request.POST, seance=seance)
        if form.is_valid():
            selected_seats = form.cleaned_data['show_start']
            return redirect('select_ticket_type')
    else:
        form = SeatForm(seance=seance)

    template = "cinema/select_seance.html"
    return render(request, template, {'form': form, 'movie': movie})

# Widok wyboru typu biletu
def select_ticket(request):
    if request.method == 'POST':
        form = TicketTypeForm(request.POST)
        if form.is_valid():
            # Zapisz wybrany bilet w sesji
            request.session['selected_ticket'] = form.cleaned_data['ticket_type'].name
            return redirect('next_step')  # Następny krok, np. wybór miejsca
    else:
        form = TicketTypeForm()
    template = "cinema/select_ticket.html"
    return render(request, template, {'form': form})

