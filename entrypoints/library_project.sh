#!/bin/bash

HOST=0.0.0.0
PORT=8080

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata library_data.json
python manage.py runserver "$HOST":"$PORT"
