#!/bin/bash

# This script is used by scalingo and is meant to run only
# on Review Apps.
# When operating the first deployment of the application, it
# replaces the post deploy hook.

echo "Entering first deploy hook for Review Apps"
PG_OPTIONS="--clean --if-exists --no-owner --no-privileges --no-comments"
PG_EXCLUDE_SCHEMA="-N 'information_schema' -N '^pg_*'"
pg_dump $PG_OPTIONS $PG_EXCLUDE_SCHEMA --dbname $PARENT_DATABASE_URL --format c --file /tmp/dump.pgsql
pg_restore $PG_OPTIONS --dbname $DATABASE_URL /tmp/dump.pgsql
psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'
psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS unaccent;'

# We want to include commands from the post deploy hook as well:
bash $HOME/scripts/post_deploy.sh
echo "Completed first deploy hook"
