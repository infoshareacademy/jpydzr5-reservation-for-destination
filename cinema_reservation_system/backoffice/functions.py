import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.urls import reverse
from cinema import models


def get_reservation_data(reservation_id):
    reservation = models.Reservation.objects.get(pk=reservation_id)

    seat_reservations = models.SeatReservation.objects.filter(reservation=reservation)
    print(seat_reservations)
    # Stwórz listę biletów w żądanej strukturze
    tickets = []
    for seat_reservation in seat_reservations:
        tickets.append({
            "ticket_type_id": seat_reservation.ticket_type.id,
            "seat_id": seat_reservation.seat.id,
        })

    # Zbuduj strukturę JSON dla rezerwacji
    reservation_data = {
        "id": reservation.id if reservation.user else None,
        "user_id": reservation.user.id if reservation.user else None,
        "movie_id": reservation.seance.movie.id if reservation.seance and reservation.seance.movie else None,
        "show_start": reservation.seance.show_start.isoformat() if reservation.seance and reservation.seance.movie else None,
        "hall_id": reservation.seance.hall.id if reservation.seance and reservation.seance.movie else None,
        "cinema_id": reservation.seance.hall.cinema.id if reservation.seance and reservation.seance.hall and reservation.seance.hall.cinema else None,
        'uuid': str(reservation.uuid),
        "tickets": tickets,
    }

    # Zwróć dane jako słownik
    return reservation_data


def generate_qr_code(request,uuid):
    # Tworzenie kodu QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # qr.add_data(data)
    qr.add_data(request.build_absolute_uri(reverse('backoffice:validate_ticket', kwargs={'uuid':uuid})))
    qr.make(fit=True)

    # Konwersja kodu QR do formatu obrazu
    img = qr.make_image(fill='black', back_color='white')

    # Zapis obrazu do strumienia w pamięci
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Zwrócenie obrazu jako odpowiedź HTTP
    return HttpResponse(buffer, content_type="image/png")

