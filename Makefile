install:
	poetry install --no-root

migrations:
	poetry run python manage.py makemigrations

superuser:
	poetry run python manage.py createsuperuser

migrate:
	poetry run python manage.py migrate

run-server:
	poetry run python manage.py runserver 127.0.0.1:8000

shell:
	poetry run python manage.py shell

export-requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: install migrations superuser migrate run-server update run;

