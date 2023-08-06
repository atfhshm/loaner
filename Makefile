install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

superuser:
	poetry run python manage.py createsuperuser

migrate:
	poetry run python manage.py migrate


run-server:
	poetry run python manage.py runserver


update: install migrate;

.PHONY install makemigrations superuser migrate runserver update;

