from collections import defaultdict

import plotly.graph_objs as go
import plotly.io as pio
import base64
from django.db.models import Count, Q, When, Case, IntegerField, F, TimeField, DateTimeField, ExpressionWrapper
from cinema import models
from django.db.models.functions import TruncMinute, Trunc, ExtractWeekDay
from django.utils.safestring import mark_safe
from datetime import timedelta

from plotly.subplots import make_subplots

DAYS_OF_WEEK = {
    0: "Niedziela",
    1: "Poniedziałek",
    2: "Wtorek",
    3: "Środa",
    4: "Czwartek",
    5: "Piątek",
    6: "Sobota",
}

def round_to_nearest_half_hour(dt):
    """Pomocnicza funkcja do zaokrąglania daty do najbliższej pół godziny"""
    discard = timedelta(minutes=dt.minute % 30, seconds=dt.second, microseconds=dt.microsecond)
    return dt - discard + (timedelta(minutes=30) if discard >= timedelta(minutes=15) else timedelta())


def best_ticket_types_chart(cinema, range_begin, range_end):
    ticket_data = models.SeatReservation.objects.filter(
        reservation__seance__hall__cinema=cinema,
        reservation__seance__show_start__gte=range_begin,
        reservation__seance__show_start__lte=range_end
    ).values('ticket_type__name').annotate(
        used=Count(Case(
            When(Q(reservation__used=True), then=1),
            output_field=IntegerField()
        )),
        unused_paid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=True), then=1),
            output_field=IntegerField()
        )),
        unused_unpaid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=False), then=1),
            output_field=IntegerField()
        ))
    )

    labels = [ticket['ticket_type__name'] for ticket in ticket_data]
    used_values = [ticket['used'] for ticket in ticket_data]
    unused_paid_values = [ticket['unused_paid'] for ticket in ticket_data]
    unused_unpaid_values = [ticket['unused_unpaid'] for ticket in ticket_data]

    # Tworzenie subplotów dla wykresów kołowych
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]],
        subplot_titles=[
            "Wykorzystane", "Zapłacone, ale niewykorzystane",
            "Niezapłacone"
        ]
    )

    # Dodawanie danych do poszczególnych wykresów kołowych
    fig.add_trace(go.Pie(labels=labels, values=used_values, hole=0.3), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels, values=unused_paid_values, hole=0.3), row=1, col=2)
    fig.add_trace(go.Pie(labels=labels, values=unused_unpaid_values, hole=0.3), row=1, col=3)

    # Ustawienia dla całego wykresu
    fig.update_layout(
        title=f"okres od {range_begin} do {range_end}",
        height=500,
    )

    # Konwertowanie wykresu na HTML
    return mark_safe(pio.to_html(fig, full_html=False))


def best_days_of_week_chart(cinema, range_begin, range_end):
    seat_reservations = models.SeatReservation.objects.filter(
        reservation__seance__hall__cinema=cinema,
        reservation__seance__show_start__gte=range_begin,
        reservation__seance__show_start__lte=range_end
    ).annotate(
        weekday=ExtractWeekDay('reservation__seance__show_start')
    ).values('weekday').annotate(
        used=Count(Case(
            When(Q(reservation__used=True), then=1),
            output_field=IntegerField()
        )),
        unused_paid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=True), then=1),
            output_field=IntegerField()
        )),
        unused_unpaid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=False), then=1),
            output_field=IntegerField()
        ))
    )

    # Grupowanie wyników po dniach tygodnia dla każdej kombinacji `used` i `paid`
    aggregated_data = defaultdict(lambda: {'used': 0, 'unused_paid': 0, 'unused_unpaid': 0})
    for reservation in seat_reservations:
        weekday = reservation['weekday']
        aggregated_data[weekday]['used'] += reservation['used']
        aggregated_data[weekday]['unused_paid'] += reservation['unused_paid']
        aggregated_data[weekday]['unused_unpaid'] += reservation['unused_unpaid']

    # Przygotowanie danych dla każdego wykresu
    labels = [DAYS_OF_WEEK[day - 1] for day in sorted(aggregated_data.keys())]

    used_values = [aggregated_data[day]['used'] for day in sorted(aggregated_data.keys())]
    unused_paid_values = [aggregated_data[day]['unused_paid'] for day in sorted(aggregated_data.keys())]
    unused_unpaid_values = [aggregated_data[day]['unused_unpaid'] for day in sorted(aggregated_data.keys())]

    # Tworzenie subplotów dla wykresów kołowych
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]],
        subplot_titles=[
            "Wykorzystane", "Zapłacone, ale niewykorzystane",
            "Niezapłacone"
        ]
    )

    # Dodawanie danych do poszczególnych wykresów kołowych
    fig.add_trace(go.Pie(labels=labels, values=used_values, hole=0.3), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels, values=unused_paid_values, hole=0.3), row=1, col=2)
    fig.add_trace(go.Pie(labels=labels, values=unused_unpaid_values, hole=0.3), row=1, col=3)

    # Ustawienia dla całego wykresu
    fig.update_layout(
        title=f"okres od {range_begin} do {range_end}",
        height=500,
    )

    # Konwertowanie wykresu na HTML
    return mark_safe(pio.to_html(fig, full_html=False))


def best_hours_chart(cinema, range_begin, range_end):
    seat_reservations = models.SeatReservation.objects.filter(
        reservation__seance__hall__cinema=cinema,
        reservation__seance__show_start__gte=range_begin,
        reservation__seance__show_start__lte=range_end
    ).annotate(
        rounded_start=ExpressionWrapper(
            Case(
                When(
                    reservation__seance__show_start__minute__lt=30,
                    then=Trunc('reservation__seance__show_start', 'hour')
                ),
                When(
                    reservation__seance__show_start__minute__gte=30,
                    then=Trunc('reservation__seance__show_start', 'hour') + timedelta(minutes=30)
                ),
            ),
            output_field=DateTimeField()
        )
    ).values('rounded_start').annotate(
        used=Count(Case(
            When(Q(reservation__used=True), then=1),
            output_field=IntegerField()
        )),
        unused_paid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=True), then=1),
            output_field=IntegerField()
        )),
        unused_unpaid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=False), then=1),
            output_field=IntegerField()
        )),
        total_reserved_seats=(
                F('used') + F('unused_paid') + F('unused_unpaid')
        )
    ).order_by('rounded_start')

    aggregated_data = defaultdict(lambda: {'used': 0, 'unused_paid': 0, 'unused_unpaid': 0})
    for reservation in seat_reservations:
        rounded_start = reservation['rounded_start'].strftime('%H:%M')
        aggregated_data[rounded_start]['used'] += reservation['used']
        aggregated_data[rounded_start]['unused_paid'] += reservation['unused_paid']
        aggregated_data[rounded_start]['unused_unpaid'] += reservation['unused_unpaid']

    # Przygotowanie danych do wykresu
    time_labels = sorted(aggregated_data.keys())
    used_counts = [aggregated_data[label]['used'] for label in time_labels]
    unused_paid_counts = [aggregated_data[label]['unused_paid'] for label in time_labels]
    unused_unpaid_counts = [aggregated_data[label]['unused_unpaid'] for label in time_labels]

    # Tworzenie wykresu słupkowego poziomego
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=used_counts,
        y=time_labels,
        orientation='h',
        name='Wykorzystane',
        marker=dict(color='green')
    ))
    fig.add_trace(go.Bar(
        x=unused_paid_counts,
        y=time_labels,
        orientation='h',
        name='Zapłacone, ale niewykorzystane',
        marker=dict(color='orange')
    ))
    fig.add_trace(go.Bar(
        x=unused_unpaid_counts,
        y=time_labels,
        orientation='h',
        name='Zarezerwowane',
        marker=dict(color='red')
    ))
    fig.update_layout(
        title=f"okres od {range_begin} do {range_end}",
        xaxis_title="Zarezerwowanych miejsc",
        yaxis_title='godziny rozpoczęcia',
        height=800,
        barmode='stack'
    )

    # Konwertowanie wykresu na HTML
    return mark_safe(pio.to_html(fig, full_html=False))


def movies_with_reservations_chart(cinema, range_begin, range_end):
    seat_reservations = models.SeatReservation.objects.filter(
        reservation__seance__hall__cinema=cinema,
        reservation__seance__show_start__gte=range_begin,
        reservation__seance__show_start__lte=range_end
    ).values('reservation__seance__movie__title').annotate(
        used=Count(Case(
            When(Q(reservation__used=True), then=1),
            output_field=IntegerField()
        )),
        unused_paid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=True), then=1),
            output_field=IntegerField()
        )),
        unused_unpaid=Count(Case(
            When(Q(reservation__used=False) & Q(reservation__paid=False), then=1),
            output_field=IntegerField()
        )),
        total_reserved_seats = (
            F('used') + F('unused_paid') + F('unused_unpaid')
        )
    ).order_by('-total_reserved_seats')

    # Przygotowanie danych do wykresu
    movie_names = [reservation['reservation__seance__movie__title'] for reservation in seat_reservations]
    used_counts = [reservation['used'] for reservation in seat_reservations]
    unused_paid_counts = [reservation['unused_paid'] for reservation in seat_reservations]
    unused_unpaid_counts = [reservation['unused_unpaid'] for reservation in seat_reservations]

    # Tworzenie wykresu słupkowego poziomego
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=used_counts,
        y=movie_names,
        orientation='h',
        name='Wykorzystane',
        marker=dict(color='green')
    ))
    fig.add_trace(go.Bar(
        x=unused_paid_counts,
        y=movie_names,
        orientation='h',
        name='Zapłacone, ale niewykorzystane',
        marker=dict(color='orange')
    ))
    fig.add_trace(go.Bar(
        x=unused_unpaid_counts,
        y=movie_names,
        orientation='h',
        name='Zarezerwowane',
        marker=dict(color='red')
    ))
    fig.update_layout(
        title=f"okres od {range_begin} do {range_end}",
        xaxis_title="Zarezerwowanych miejsc",
        yaxis_title='Film',
        height=800,
        barmode='stack'
    )

    # Konwertowanie wykresu na HTML
    return mark_safe(pio.to_html(fig, full_html=False))
