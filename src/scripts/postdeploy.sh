#!/bin/bash
echo "Entering postdeploy hook"

if [ "$IS_REVIEW_APP" = "true" ] ; then
  echo "    Review Apps : Database copy"
  pg_dump $STAGING_DATABASE_URL | psql $DATABASE_URL
fi

python manage.py migrate
python manage.py compilemessages
python manage.py compress --force
echo "Completed postdeploy hook"
