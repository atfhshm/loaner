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

shell:
	poetry run python manage.py shell

.PHONY: install migrations superuser migrate run-server update run;

