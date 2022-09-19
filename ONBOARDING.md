# Onboarding tech

## Montage de l'environnement de travail

La procédure est documentée [ici](https://github.com/MTES-MCT/aides-territoires/wiki/Installation-de-l'environment-en-local).


### Lancement des tests

Pour lancer les tests depuis la machine virtuelle il est nécessaire que l'utilisateur `postgres` donne l'autorisation à l'utilisateur `aides` de créer une base de données :

    su - postgres
    psql alter user aides createdb

Il faut aussi installer l'extension pg_trgm :

    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS pg_trgm;' -U postgres
    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS unaccent;' -U postgres
    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS btree_gin;' -U postgres
    psql -d template1 -c 'CREATE TEXT SEARCH CONFIGURATION french_unaccent( COPY = french ); ALTER TEXT SEARCH CONFIGURATION french_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;' -U postgres

Ensuite, l'utilisateur `aides` peut lancer les tests :

    su - aides
    cd aides/src
    make test
