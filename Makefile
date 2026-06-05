SHELL 		:= /bin/bash
UV			:= uv
VENV_DIR	:= .venv

.PHONY: venv install uninstall clean test test-all lint format build docs

install:
	$(UV) sync --all-extras

uninstall:
	rm -rf $(VENV_DIR)

clean:
	rm -rf build/ dist/ src/*.egg-info **/__pycache__ .coverage .pytest_cache/ .ruff_cache/

test:
	$(UV) run pytest tests/unit

test-all:
	$(UV) run pytest tests

lint:
	$(UV) run ruff format --check src tests
	$(UV) run ruff check src tests

format:
	$(UV) run ruff format src tests
	$(UV) run ruff check --select I001 --fix src tests # Only fixes import order

build:
	$(UV) build

docs:
	rm -f docs/reference/_autosummary/*.rst
	$(UV) run sphinx-build -b html docs/ build/docs/
