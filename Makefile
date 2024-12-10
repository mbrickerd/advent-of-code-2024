.DEFAULT: help

help:
	@echo "make install"
	@echo "       install all dependencies specified in pyproject.toml"
	@echo "make lint"
	@echo "       run flake8 checks"
	@echo "make format"
	@echo "       run isort and black to format code"
	@echo "make check"
	@echo "       run all code quality checks (format + lint)"
	@echo "make test"
	@echo "       run pytest"
	@echo "make all"
	@echo "       run format, lint, and test"
	@echo "make help"
	@echo "       print this help message"

install:
	poetry install

lint:
	poetry run flake8 .

format:
	poetry run isort .
	poetry run black .

check: format lint

test:
	poetry run pytest tests/

all: format lint test

.PHONY: help install lint format check test all