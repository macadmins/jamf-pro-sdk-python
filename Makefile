SHELL := /bin/bash
.PHONY: docs

install:
	python3 -m pip install --upgrade --force-reinstall --editable '.[dev]'

uninstall:
	python3 -m pip uninstall -y -r <(python3 -m pip freeze)

clean:
	rm -rf build/ dist/ src/*.egg-info **/__pycache__ .coverage .pytest_cache/ .ruff_cache/

test:
	pytest tests/unit

test-all:
	pytest tests

lint:
	ruff format --check src tests
	ruff check src tests

format:
	ruff format src tests
	ruff check --select I001 --fix src tests # Only fixes import order

build:
	python3 -m build --sdist --wheel

docs:
	rm -f docs/reference/_autosummary/*.rst
	sphinx-build -b html docs/ build/docs/
