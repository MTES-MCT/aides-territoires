#!/bin/bash
echo "Entering firstdeploy hook for Review Apps"
pg_dump --clean --if-exists --dbname $STAGING_DATABASE_URL --no-owner --no-privileges --no-comments --exclude-schema 'information_schema' --exclude-schema '^pg_*' | psql $DATABASE_URL
bash postdeploy.sh
echo "Completed firstdeploy hook"
