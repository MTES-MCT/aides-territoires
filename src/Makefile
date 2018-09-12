init:
	pipenv || pip install pipenv
	pipenv install --dev
	npm install
	pipenv run python manage.py collectstatic --settings=core.settings.test

test:
	pipenv run py.test

checkstyle:
	pipenv run flake8 --config=flake8.ini

makemessages:
	pipenv run python manage.py makemessages --all --no-location --no-obsolete
