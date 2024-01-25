.PHONY: test

all: help

lint:
	flake8 .

test:
	pytest -v ./test

build:
	poetry build

help:
	@echo "No description yet!"
