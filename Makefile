.PHONY: test

all: help

lint:
	flake8 .

test:
	pytest -v ./tests -s

build:
	poetry build

help:
	@echo "No description yet!"
