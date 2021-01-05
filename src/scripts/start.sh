#!/bin/bash

echo "Entering deployment start script"
python manage.py compilemessages
gunicorn core.wsgi_scalingo --log-file -
echo "Completed deployment start script"
