#!/bin/bash

# This script is used by scalingo each time the application
# is deployed.
# For review apps, if a first-deploy hook is defined, then
# that first deploy hook will override this postdeploy hook.

echo "Entering postdeploy hook"
python manage.py migrate
python manage.py compress --force
echo "Completed postdeploy hook"
