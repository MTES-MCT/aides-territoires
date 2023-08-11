# Loading environment variables
ifneq (,$(wildcard ./.env.local))
    include .env.local
    export LOCAL_PATH, LOCAL_PATH_PP
endif

# Setting defaults for env variables
ifdef LOCAL_PATH
	local_path := $(LOCAL_PATH)
else
	local_path := aides-territoires.localhost:8000
endif

ifdef LOCAL_PATH_PP
	local_path_pp := $(LOCAL_PATH_PP)
else
	local_path_pp := francemobilites.aides-territoires.localhost:8001
endif

init:
	pipenv sync --dev
	npm ci

build:
	pipenv run python manage.py collectstatic --settings=core.settings.test --no-input
	pipenv run python manage.py compilemessages --settings=core.settings.test
	pipenv run python manage.py compress --force

test:
	pipenv run py.test $(app) -v -n 10

check:
	pipenv run python manage.py check

coverage:
	pipenv run coverage run --source='.' -m pytest $(app) && pipenv run coverage html
# for a single app: call with `make app=aids coverage`

checkstyle:
	pipenv run ruff check .

makemessages:
	pipenv run python manage.py makemessages --all --no-obsolete

css:
	sassc -I $(include) $(infile) $(outfile)

fullcss:
	sassc -I $(include) $(infile) $(outfile)
	./node_modules/.bin/postcss --use autoprefixer -r $(outfile) --no-map

compress:
	pipenv run python manage.py compress --force

dev-set-local-domain:
	pipenv run python manage.py dev_set_local_domain --site_path=$(local_path)

runserver:
	pipenv run python manage.py runserver $(local_path)

runserver_pp:
	pipenv run python manage.py runserver $(local_path_pp) --settings minisites.settings.local
