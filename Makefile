install:
	poetry install --no-root

migrations:
	poetry run python manage.py makemigrations

superuser:
	poetry run python manage.py createsuperuser

migrate:
	poetry run python manage.py migrate

run-server:
	poetry run python manage.py runserver

.PHONY: install migrations superuser migrate run-server update run;

