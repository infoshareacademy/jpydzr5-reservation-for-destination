#!/bin/bash
cd ../cinema_reservation_system
python manage.py loaddata cinema/fixtures/cinemas.json
python manage.py loaddata cinema/fixtures/halls.json
python manage.py loaddata cinema/fixtures/movies.json
python manage.py loaddata cinema/fixtures/prices.json
cd ..
