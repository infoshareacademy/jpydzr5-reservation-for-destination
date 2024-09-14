#!/bin/sh -x
cd ../cinema_reservation_system
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata cinema/fixtures/users.json
python manage.py loaddata cinema/fixtures/cinemas.json
python manage.py loaddata cinema/fixtures/halls.json
python manage.py loaddata cinema/fixtures/movies.json
python manage.py loaddata cinema/fixtures/ticket_types.json
python manage.py loaddata cinema/fixtures/seat_types.json
python manage.py loaddata cinema/fixtures/seats.json
python manage.py loaddata cinema/fixtures/reservations.json
python manage.py loaddata cinema/fixtures/seat_reservations.json
cd ..
