#!/bin/sh -x
cd ../cinema_reservation_system
pip install -r requirements.txt
python manage.py migrate
../tools/loaddata.sh
echo "please wait - generating seances"
python manage.py generate_seances
echo "please wait - generating reservations"
python manage.py generate_reservations
cd -
clear
echo "end of upgrading. Thank you"
echo "Press Enter, to continue ..."
read

