.PHONY: help install lint lint-fix format check test type-check all setup-pre-commit fix-all

.DEFAULT: help

help:
	@echo "make install"
	@echo "       install all dependencies specified in pyproject.toml using uv"
	@echo "make setup-pre-commit"
	@echo "       set up pre-commit hooks"
	@echo "make lint"
	@echo "       run ruff linting checks"
	@echo "make lint-fix"
	@echo "       run ruff linting checks and fix auto-fixable issues"
	@echo "make format"
	@echo "       run ruff format to format code and organize imports"
	@echo "make type-check"
	@echo "       run mypy for type checking"
	@echo "make check"
	@echo "       run all code quality checks (format + lint + type-check)"
	@echo "make fix-all"
	@echo "       run all auto-fixes (format + lint-fix)"
	@echo "make test"
	@echo "       run pytest"
	@echo "make all"
	@echo "       run format, lint, type-check, and test"
	@echo "make help"
	@echo "       print this help message"

install:
	uv pip install -e ".[dependency-groups.dev]"
	$(MAKE) setup-pre-commit

setup-pre-commit:
	pre-commit install

lint:
	ruff check .

lint-fix:
	ruff check --fix .

format:
	ruff format .

type-check:
	mypy .

check: format lint type-check

fix-all: format lint-fix

test:
	pytest tests/

all: format lint type-check test
