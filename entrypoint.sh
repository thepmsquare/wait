#!/bin/sh

# exit immediately if a command exits with a non-zero status.
set -e

# Generates a key only when one was not supplied. Set SECRET_KEY in production
# so that sessions survive container restarts.
if [ -z "${SECRET_KEY:-}" ]; then
  SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
  export SECRET_KEY
  echo "warning: SECRET_KEY was not provided; generated an ephemeral key."
fi

# run migrations (set RUN_MIGRATIONS=0 when running multiple replicas)
if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
  echo "applying database migrations..."
  python manage.py migrate --no-input
fi

# allow overriding the default command (e.g. one-off management commands)
if [ "$#" -gt 0 ]; then
  exec "$@"
fi

# serve the application
echo "starting gunicorn..."
exec gunicorn \
  --bind "0.0.0.0:${PORT:-30001}" \
  --workers "${GUNICORN_WORKERS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --access-logfile - \
  wait.wsgi:application
