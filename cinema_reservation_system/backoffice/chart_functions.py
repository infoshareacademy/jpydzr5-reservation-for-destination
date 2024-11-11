from django.db.models import Count, Case, When, Q, IntegerField
from django.utils.safestring import mark_safe
from plotly import graph_objs as go, io as pio
from plotly.subplots import make_subplots


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
