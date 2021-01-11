#!/bin/bash

# This script is used by scalingo and is meant to run only
# on Review Apps.
# When operating the first deployment of the application, it
# replaces the post deploy hook.

echo "Entering first deploy hook for Review Apps"
pg_dump --clean --if-exists --dbname $STAGING_DATABASE_URL --no-owner --no-privileges --no-comments | psql $DATABASE_URL

# We want to include commands from the post deploy hook as well:
bash $HOME/scripts/post_deploy.sh
echo "Completed first deploy hook"
