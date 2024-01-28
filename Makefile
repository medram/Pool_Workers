.PHONY: test

all: help

lint:
	flake8 .

test:	lint mypy coverage # Run all the tests


pytest:
	pytest -vs ./tests

coverage:
	coverage run --source ./pool_workers -m pytest -vs ./tests && coverage report

mypy:
	mypy --check-untyped-defs pool_workers/

build:
	poetry build

publish: dist
	twine upload dist/*

clean:
	rm -fr .coverage .pytest_cache .mypy_cache htmlcov

help:
	@echo "No description yet!"
