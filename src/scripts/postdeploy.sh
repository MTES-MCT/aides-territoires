#!/bin/bash
echo "Entering postdeploy hook"
python manage.py migrate
python manage.py compress --force
echo "Completed postdeploy hook"
