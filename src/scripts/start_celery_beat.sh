#!/bin/bash

# This script is used by scalingo to start the the application
# It run every time the app container starts, for instance,
# after a deployment or when the container is restarted.

echo "Entering start celery event script"
echo "Using Django settings module: $DJANGO_SETTINGS_MODULE"
python manage.py compilemessages
celery -A core worker --beat  --concurrency=${CELERY_BEAT_CONCURRENCY:=4} --loglevel info
echo "Completed start celery beat script"
