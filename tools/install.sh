#!/usr/bin/env bash
cd ../cinema_reservation_system
pip install -r requirements.txt
python manage.py migrate
clear
echo "Please createsuperuser."
echo "python manage.py createsuperuser"
echo "and then"
echo "tools/upgrade.sh"
echo
echo "Press Enter, to continue ..."
read
