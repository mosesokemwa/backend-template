.PHONY: install install-pre-commit pre-commit-install pre-commit-update lint migrate migrations shell dbshell clean superuser test update run
install:
	python -m pip install --upgrade pip
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

pre-commit-install:
	pre-commit uninstall; pre-commit install

pre-commit-update:
	pre-commit autoupdate

lint:
	pre-commit run --all-files

migrate:
	python -m manage migrate

migrations:
	python -m manage makemigrations

shell:
	python -m manage shell

dbshell:
	python -m manage dbshell

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

superuser:
	python -m manage createsuperuser

test:
	python -m manage test

update: install migrate install-pre-commit ;

run:
	python -m manage runserver
