#!/bin/bash

#set -euo pipefail

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixture-ingredients.json fixture-measures.json

if [[ "$DJANGO_ENV" = "PRODUCTION" ]]; then
  gunicorn -b 0.0.0.0:8000 \
    --log-level ${DJANGO_LOG_LEVEL,,} \
    --access-logfile - config.wsgi:application
else
  python manage.py runserver 0.0.0.0:8000
fi