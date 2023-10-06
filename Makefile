PYTHON_INTERPRETER = python3
DJANGO_MANAGE = ./manage.py
RUNSERVER_PORT = 8000

install:
    pip install -r requirements.txt

makemigrations:
    $(PYTHON_INTERPRETER) $(DJANGO_MANAGE) makemigrations

migrate:
    $(PYTHON_INTERPRETER) $(DJANGO_MANAGE) migrate

runserver:
    $(PYTHON_INTERPRETER) $(DJANGO_MANAGE) runserver $(RUNSERVER_PORT)

createsuperuser:
    $(PYTHON_INTERPRETER) $(DJANGO_MANAGE) createsuperuser

test:
    $(PYTHON_INTERPRETER) $(DJANGO_MANAGE) test

.PHONY: install makemigrations migrate runserver createsuperuser test
