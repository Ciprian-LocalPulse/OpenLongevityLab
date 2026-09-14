.PHONY: install test lint format typecheck
install:
	python -m pip install -e ".[dev,api]"
test:
	pytest
lint:
	ruff check .
format:
	ruff format .
typecheck:
	mypy src
