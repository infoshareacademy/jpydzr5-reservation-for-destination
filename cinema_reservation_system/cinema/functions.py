
from . import models


def free_seats_for_seance(seance):
    # Pobierz wszystkie miejsca w sali, w której odbywa się seans
    all_seats = seance.hall.seat_set.all()

    # Pobierz wszystkie zarezerwowane miejsca dla tego seansu
    reserved_seats = models.SeatReservation.objects.filter(
        reservation__seance=seance,
        reservation__cancelled=False
    ).values_list('seat', flat=True)

    # Oblicz liczbę wolnych miejsc
    free_seats = all_seats.exclude(id__in=reserved_seats)

    # Filtruj wolne miejsca dla osób niepełnosprawnych
    free_disabled_seats = free_seats.filter(seat_type__id=3)
    free_notdisabled_seats = free_seats.exclude(seat_type__id=3)
    return {
        'free_seats_count': free_notdisabled_seats.count(),
        'free_disabled_seats_count': free_disabled_seats.count(),

    }

