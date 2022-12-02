init:
	pipenv sync --dev
	npm ci

build:
	pipenv run python manage.py collectstatic --settings=core.settings.test --no-input
	pipenv run python manage.py compilemessages --settings=core.settings.test
	pipenv run python manage.py compress --force

test:
	pipenv run py.test -v -n 10

checkstyle:
	pipenv run flake8 --config=.flake8

makemessages:
	pipenv run python manage.py makemessages --all --no-location --no-obsolete

css:
	sassc -I $(include) $(infile) $(outfile)

fullcss:
	sassc -I $(include) $(infile) $(outfile)
	./node_modules/.bin/postcss --use autoprefixer -r $(outfile) --no-map
