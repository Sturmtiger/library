#!/bin/bash

HOST=0.0.0.0
PORT=8080

celery -A Library.celery_app worker --detach -B -l INFO -Q send_mail

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata library_data_social.json
python manage.py runserver "$HOST":"$PORT"
