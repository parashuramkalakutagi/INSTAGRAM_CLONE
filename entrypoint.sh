#!/bin/sh

python manage.py makemigrations
python manage.py migrate



gunicorn -b 0.0.0.0 -p 8000  instagram.wsgi:application
celery  -A instagram.celery worker --pool=solo -l info
celery -A instagram beat -l info
