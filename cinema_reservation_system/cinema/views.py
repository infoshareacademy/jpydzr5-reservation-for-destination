from django.template.response import TemplateResponse
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
from django.template.response import TemplateResponse
from django.shortcuts import redirect

# Widok koszyka
def basket(request):
    # Ścieżka do szablonu
    template = "cinema/basket.html"

    # Sprawdź, czy w sesji są jakieś dane koszyka (wybrany seans, bilet, etc.)
    selected_seance = request.session.get('selected_seance')
    selected_ticket = request.session.get('selected_ticket')

    # Jeśli użytkownik nie wybrał jeszcze seansu ani biletu, wyślij go do wyboru seansu
    if not selected_seance or not selected_ticket:
        return redirect('select_seance')

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
    message = {"message": "OK!"}
    return TemplateResponse(request, template, message)


from django.shortcuts import render, redirect
from .forms import SeanceForm, TicketTypeForm

def select_seance(request):
    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            # Zapisz dane seansu w sesji
            request.session['selected_seance'] = form.cleaned_data['movie'].title
            return redirect('select_ticket')
    else:
        form = SeanceForm()
    template = "cinema/select_seance.html"
    return render(request, template, {'form': form})

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

