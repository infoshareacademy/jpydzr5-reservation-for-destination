#!/bin/sh
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Brak aktywnego środowiska wirtualnego. Zakończono działanie."
    exit 1
fi
olddir=$(pwd)
cd "$(dirname "$VIRTUAL_ENV")"/cinema_reservation_system
pip install -r requirements.txt
python manage.py migrate
sh $(dirname "$VIRTUAL_ENV")/tools/loaddata.sh
echo "please wait - generating seances"
python manage.py generate_seances
echo "please wait - generating reservations"
python manage.py generate_reservations
cd "$olddir"
clear
echo "end of upgrading. Thank you"
echo "Press Enter, to continue ..."
read

