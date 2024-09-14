#!/bin/bash
pip install -r requirements.txt
cd ../cinema_reservation_system
python manage.py loaddata cinema/fixtures/users.json
python manage.py loaddata cinema/fixtures/cinemas.json
python manage.py loaddata cinema/fixtures/halls.json
python manage.py loaddata cinema/fixtures/movies.json
python manage.py loaddata cinema/fixtures/ticket_types.json
python manage.py dumpdata cinema/fixtures/seat_types.json
python manage.py dumpdata cinema/fixtures/seats.json
python manage.py dumpdata cinema/fixtures/reservations.json
python manage.py dumpdata cinema/fixtures/seat_reservations.json
cd ..
