#!/usr/bin/env bash
python manage.py makemigrations --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py load_ingredients
gunicorn foodgram.wsgi:application --bind 0:8000