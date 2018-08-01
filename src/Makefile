init:
	pipenv || pip install pipenv
	pipenv install --dev
	npm install
	pipenv run python manage.py collectstatic

test:
	pipenv run py.test

checkstyle:
	pipenv run flake8
