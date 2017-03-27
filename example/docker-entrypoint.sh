#!/bin/bash

# Wait until postgres is ready
until nc -z $DATABASE_HOST 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 3
done

echo Running migrations
python manage.py migrate --noinput

echo Collecting static-files
python manage.py collectstatic --noinput

echo Starting using manage.py runserver
python manage.py runserver 0.0.0.0:8000
