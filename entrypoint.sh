#!/bin/sh

# exit immediately if a command exits with a non-zero status.
set -e

# run migrations
echo "applying database migrations..."
python manage.py migrate --no-input

# serve the application
echo "starting gunicorn..."
exec gunicorn --bind 0.0.0.0:30001 wait.wsgi:application
