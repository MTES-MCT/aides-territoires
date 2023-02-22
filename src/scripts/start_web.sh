#!/bin/bash

# This script is used by scalingo to start the application
# It run every time the app container starts, for instance,
# after a deployment or when the container is restarted.

echo "Entering start web script"
echo "Using Django settings module: $DJANGO_SETTINGS_MODULE"
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py compress --force
gunicorn core.wsgi_scalingo --timeout 90 --log-file -
echo "Completed start web script"
