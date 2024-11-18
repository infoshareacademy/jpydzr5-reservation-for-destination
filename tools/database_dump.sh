#!/bin/bash
cd ../cinema_reservation_system
python manage.py dumpdata cinema.cinema --indent 2 > cinema/fixtures/cinemas.json
python manage.py dumpdata cinema.hall --indent 2 > cinema/fixtures/halls.json
# źle działa pod windowsem
#python manage.py dumpdata cinema.movie --indent 2 > cinema/fixtures/movies.json
python manage.py dumpdata cinema.tickettype --indent 2 > cinema/fixtures/ticket_types.json
python manage.py dumpdata cinema.seattype --indent 2 > cinema/fixtures/seat_types.json
python manage.py dumpdata cinema.seance --indent 2 > cinema/fixtures/seances.json
python manage.py dumpdata cinema.seat --indent 2 > cinema/fixtures/seats.json
python manage.py dumpdata cinema.reservation --indent 2 > cinema/fixtures/reservations.json
python manage.py dumpdata cinema.seatreservation --indent 2 > cinema/fixtures/seat_reservations.json
cd ..
