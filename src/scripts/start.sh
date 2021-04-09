#!/bin/bash

# This script is used by scalingo to start the web application
# It run every time the app container starts, for instance, 
# after a deployment or when the container is restarted.

echo "Entering deployment start script"
export DJANGO_SETTINGS_MODULE=$1
if [ -z "$DJANGO_SETTINGS_MODULE" ]
  then
    echo "The start script expects the DJANGO_SETTINGS_MODULE as first argument"
fi
echo "Using Django settings module: $DJANGO_SETTINGS_MODULE"
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py compress --force
gunicorn core.wsgi_scalingo --log-file -
echo "Completed deployment start script"
