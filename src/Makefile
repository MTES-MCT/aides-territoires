init:
	pipenv sync --dev
	npm ci
	pipenv run python manage.py collectstatic --settings=core.settings.test --no-input
	pipenv run python manage.py compilemessages --settings=core.settings.test

test:
	pipenv run py.test -v --nomigrations

checkstyle:
	pipenv run flake8 --config=flake8.ini

makemessages:
	pipenv run python manage.py makemessages --all --no-location --no-obsolete

css:
	sass -I $(include) $(infile) $(outfile)

fullcss:
	sass -I $(include) $(infile) $(outfile)
	./node_modules/.bin/postcss --use autoprefixer -r $(outfile) --no-map
