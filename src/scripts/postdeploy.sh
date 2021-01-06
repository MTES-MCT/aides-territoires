#!/bin/bash
echo "Entering postdeploy hook"

if [ "$IS_REVIEW_APP" = true ] ; then
  echo "Review Apps : Database copy"
  pg_dump --clean --if-exists --dbname $STAGING_DATABASE_URL --no-owner --no-privileges --no-comments --exclude-schema 'information_schema' --exclude-schema '^pg_*' | psql $DATABASE_URL
fi

python manage.py migrate
python manage.py compilemessages
python manage.py compress --force
echo "Completed postdeploy hook"
