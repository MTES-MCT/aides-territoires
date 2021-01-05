init:
	pipenv || pip install pipenv
	pipenv sync
	npm ci
	pipenv run python manage.py collectstatic --settings=core.settings.test
	pipenv run python manage.py compilemessages --settings=core.settings.test

test:
	pipenv run py.test

checkstyle:
	pipenv run flake8 --config=flake8.ini

makemessages:
	pipenv run python manage.py makemessages --all --no-location --no-obsolete

css:
	sass -I $(include) $(infile) $(outfile)

fullcss:
	sass -I $(include) $(infile) $(outfile)
	./node_modules/.bin/postcss --use autoprefixer -r $(outfile) --no-map
