#!/bin/sh
echo "setting users"
python manage.py loaddata cinema/fixtures/users.json
echo "setting cinemas"
python manage.py loaddata cinema/fixtures/cinemas.json
echo "setting halls"
python manage.py loaddata cinema/fixtures/halls.json
echo "setting movies"
python manage.py loaddata cinema/fixtures/movies.json
echo "setting ticket_types"
python manage.py loaddata cinema/fixtures/ticket_types.json
echo "setting seat_types"
python manage.py loaddata cinema/fixtures/seat_types.json
echo "setting seats"
python manage.py loaddata cinema/fixtures/seats.json
echo "setting seances"
python manage.py loaddata cinema/fixtures/seances.json
echo "setting reservations"
python manage.py loaddata cinema/fixtures/reservations.json
echo "setting seat_reservations"
python manage.py loaddata cinema/fixtures/seat_reservations.json

