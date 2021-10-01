#!/bin/bash


echo "Copy and restore data from prod"
PG_OPTIONS="--clean --if-exists --no-owner --no-privileges --no-comments"
pg_dump $PG_OPTIONS --dbname $PRODUCTION_DATABASE_URL --format c --file /tmp/dump.pgsql
pg_restore $PG_OPTIONS --dbname $DATABASE_URL /tmp/dump.pgsql
psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS pg_trgm;'
psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS unaccent;'
psql -d $DATABASE_URL -c 'CREATE EXTENSION IF NOT EXISTS btree_gin;' -U postgres
# make the search_vector unaccented (taken from https://stackoverflow.com/a/47248109/4293684 )
psql -d $DATABASE_URL -c 'CREATE TEXT SEARCH CONFIGURATION french_unaccent( COPY = french ); ALTER TEXT SEARCH CONFIGURATION french_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;'

# We want to include commands from the post deploy hook as well:
bash $HOME/scripts/post_deploy.sh
echo "Restore completed"
