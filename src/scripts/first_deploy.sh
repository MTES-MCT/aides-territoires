#!/bin/bash

# This script is used by scalingo and is meant to run only
# on Review Apps.
# When operating the first deployment of the application, it
# replaces the post deploy hook.

echo "Entering first deploy hook for Review Apps"
PG_OPTIONS="--clean --if-exists --no-owner --no-privileges --no-comments"
PG_EXCLUDE_TABLE="-T django_session -T actstream_action -T geofr_perimeter_contained_in -T stats_event"
pg_dump $PG_OPTIONS $PG_EXCLUDE_TABLE --dbname $STAGING_DATABASE_URL --format c --file /tmp/dump.pgsql
pg_restore $PG_OPTIONS --dbname $DATABASE_URL /tmp/dump.pgsql

# We want to include commands from the post deploy hook as well:
bash $HOME/scripts/post_deploy.sh
echo "Completed first deploy hook"
