import pendulum
from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, F, Subquery, Prefetch, Q
from django.db.models.functions import ExtractHour, ExtractMinute, ExtractWeekDay
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from backoffice.charts import movies_with_reservations_chart, best_hours_chart, best_days_of_week_chart, best_ticket_types_chart

from cinema import models
from backoffice import decorators

DAYS_OF_WEEK = {
    1: "Niedziela",
    2: "Poniedziałek",
    3: "Wtorek",
    4: "Środa",
    5: "Czwartek",
    6: "Piątek",
    7: "Sobota",
}


@login_required(login_url='login')
def index(request):
    return redirect('backoffice:dashboard')


@login_required
@decorators.set_vars
def dashboard(request, context):
    current_seance_qs = models.Seance.objects.filter(
        show_start__lte=pendulum.now(),  # seans już się rozpoczął
        show_start__gte=pendulum.now() - F('movie__duration') - F('hall__cleaning_time') # seans jeszcze trwa
    )

    halls = models.Hall.objects.filter(cinema=context['selected_cinema']).prefetch_related(
        Prefetch('seance_set',queryset=current_seance_qs, to_attr='current_seance')
    )

    for hall in halls:
        for seance in hall.current_seance:
            # Liczenie miejsc użytych (used=True) dla danego seansu
            seance.used_seats_count = models.SeatReservation.objects.filter(
                reservation__seance=seance,
                reservation__used=True
            ).count()
            seance.paid_seats_count = models.SeatReservation.objects.filter(
                reservation__seance=seance,
                reservation__paid=True
            ).count()

    message = ""
    context.update({
        'halls': halls,
        'message': message,
    })
    template = "backoffice/dashboard.html"
    return TemplateResponse(request, template, context)

@login_required
def pdf_report(request):
    return HttpResponse("Hello, world. You're at the backoffice index.")

@login_required
@decorators.set_vars
def user_panel(request, context):
    return render(request, 'backoffice/user_panel.html', {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    })



@login_required
@decorators.set_vars
def report(request, context):
    #     Stworzenie statystyki pod:
    #
    # Najczęściej wybierany film przez klienta (raport tyd/mięs)
    # Najczęściej wybierana godzina seansu przez klienta
    # Najczęściej wybierany dzień tygodnia przez klienta
    # Najczęściej wybierany rodzaj biletu przez klienta
    today = pendulum.today()
    range_end = today.add(days=1)
    range_begin = today.subtract(days=7)


    popular_ticket_types = (
        models.SeatReservation.objects.filter(
            reservation__seance__show_start__gte=range_begin,
            reservation__seance__show_start__lte=range_end,
        ).values(
            'ticket_type',
            'ticket_type__name'
        ).annotate(count=Count('id')  # Zlicza wystąpienia seansów dla każdej godziny
        ).order_by('-count')  # Sortuje według liczby wystąpień malejąco
    )

    context.update({
        'range_begin' : range_begin,
        'range_end': range_end,
        'best_hours_chart': best_hours_chart(context['selected_cinema'], range_begin, range_end),
        'best_days_of_week_chart': best_days_of_week_chart(context['selected_cinema'], range_begin, range_end),
        'best_ticket_types_chart': best_ticket_types_chart(context['selected_cinema'], range_begin, range_end),
        'movies_with_reservations_chart': movies_with_reservations_chart(context['selected_cinema'], range_begin, range_end),
    })
    return render(request, 'backoffice/report.html', context)

