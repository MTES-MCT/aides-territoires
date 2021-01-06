#!/bin/bash

# This script is used by scalingo to start the web application
# It run every time the app container starts, for instance, 
# after a deployment or when the container is restarted.

echo "Entering deployment start script"
python manage.py compilemessages
gunicorn core.wsgi_scalingo --log-file -
echo "Completed deployment start script"
