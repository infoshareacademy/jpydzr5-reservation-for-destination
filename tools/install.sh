#!/bin/sh
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Brak aktywnego środowiska wirtualnego. Zakończono działanie."
    exit 1
fi
olddir=$(pwd)
cd "$(dirname "$VIRTUAL_ENV")"/cinema_reservation_system
pip install -r requirements.txt
echo "create superuser account"
python manage.py migrate
python manage.py createsuperuser
clear
echo "now run"
echo "tools/upgrade.sh"
echo
echo "Press Enter, to continue ..."
read
