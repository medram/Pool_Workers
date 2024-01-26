.PHONY: test

all: help

lint:
	flake8 .

test:	lint mypy coverage # Run all the tests


pytest:
	pytest -vs ./tests

coverage:
	coverage run -m pytest -vs ./tests && coverage report

mypy:
	mypy --check-untyped-defs pool_workers/

build:
	poetry build

publish: dist
	twine upload dist/*

help:
	@echo "No description yet!"
