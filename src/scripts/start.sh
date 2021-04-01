#!/bin/bash

# This script is used by scalingo to start the web application
# It run every time the app container starts, for instance, 
# after a deployment or when the container is restarted.

echo "Entering deployment start script"
WSGI_MODULE=$1
if [ -z "$WSGI_MODULE" ]
  then
    echo "The start script expects the WSGI_MODULE as first argument"
fi
echo "Using WSGI module: $WSGI_MODULE"
python manage.py compilemessages
gunicorn $WSGI_MODULE --log-file -
echo "Completed deployment start script"
