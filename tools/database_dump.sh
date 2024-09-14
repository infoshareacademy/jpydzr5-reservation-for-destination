#!/bin/bash
cd ../cinema_reservation_system
python manage.py dumpdata cinema.cinema --indent 2 > cinema/fixtures/cinemas.json
python manage.py dumpdata cinema.hall --indent 2 > cinema/fixtures/halls.json
python manage.py dumpdata cinema.movie --indent 2 > cinema/fixtures/movies.json
python manage.py dumpdata cinema.tickettype --indent 2 > cinema/fixtures/ticket_types.json
cd ..
