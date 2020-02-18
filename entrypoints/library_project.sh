#!/bin/bash

host=0.0.0.0
port=8080

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata library_data.json
python manage.py runserver "$host":"$port"
