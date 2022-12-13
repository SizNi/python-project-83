dev:
	poetry run flask --app page_analyzer:app run

install: # install poetry
	poetry install

pytest:
	poetry run pytest

lint: # запуск flake8 на проект python-project-50
	poetry run flake8