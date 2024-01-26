.PHONY: test

all: help

lint:
	flake8 .

test:
	pytest -v ./tests -s

build:
	poetry build

publish: dist
	# poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
	twine upload dist/*

help:
	@echo "No description yet!"
