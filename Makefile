.PHONY: test

all: help

lint:	flake8 mypy

test:	lint mypy coverage # Run all the tests

pytest:
	pytest -vs ./tests

coverage:
	coverage run --source ./pool_workers -m pytest -vs ./tests
	coverage report --fail-under=90

flake8:
	flake8 ./pool_workers ./tests

mypy:
	mypy --check-untyped-defs ./pool_workers ./tests

tox:
	tox p -e ALL

build:
	poetry build

publish: dist
	twine upload dist/*

clean:
	rm -fr .coverage .pytest_cache .mypy_cache htmlcov .tox dist

help:
	@echo "No description yet!"
