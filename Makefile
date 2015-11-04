PROJECT_DIR=$(shell pwd)
VENV_DIR?=$(PROJECT_DIR)/.env
PIP?=$(VENV_DIR)/bin/pip
PYTHON?=$(VENV_DIR)/bin/python
NOSE?=$(VENV_DIR)/bin/nosetests

.PHONY: all clean test run requirements install virtualenv

all: virtualenv install create_database create_admin test

virtualenv:
	virtualenv $(VENV_DIR)

install: requirements

requirements:
	$(PIP) install -r $(PROJECT_DIR)/requirements.txt

create_database:
	$(PYTHON) manage.py syncdb --noinput
	$(PYTHON) manage.py migrate --noinput
	$(PYTHON) manage.py makemigrations
	find src/apps -name '*.json' -exec $(PYTHON) manage.py loaddata {} \;

create_admin:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@site.com', '12345')" | $(PYTHON) manage.py shell

run:
	$(PYTHON) manage.py runserver

migrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

collect:
	$(PYTHON) manage.py collectstatic

shell:
	$(PYTHON) manage.py shell

test:
	$(PYTHON) manage.py test src/apps --verbosity=1 --logging-level=ERROR

clean_temp:
	find . -name '*.pyc' -delete
	rm -rf .coverage dist docs/_build htmlcov MANIFEST

clean_venv:
	rm -rf $(VENV_DIR)

clean: clean_temp clean_venv

