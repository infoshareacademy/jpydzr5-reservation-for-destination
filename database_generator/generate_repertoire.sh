cd ../cinema_reservation_system
python manage.py loaddata movies.json
python manage.py loaddata prices.json
cd ../database_generator
python runner.py
cd ..