dev:
	poetry run flask --app page_analyzer/app:app run

install: # install poetry
	poetry install

pytest:
	poetry run pytest

lint: # запуск flake8 на проект python-project-50
	poetry run flake8

# запуск сервера в продакшене по адресу http://localhost:8000 
#если в переменных окружения не указан порт (он необходим для деплоя приложения)
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
