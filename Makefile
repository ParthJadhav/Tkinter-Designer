.PHONY: setup test lint build check cli gui clean

PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -e . pytest flake8 build

test:
	$(BIN)/python -m pytest -q

lint:
	$(BIN)/flake8 . --exclude=$(VENV)

build:
	$(BIN)/python -m build

check: lint test build

cli:
	$(BIN)/tkdesigner --inspect "$(FIGMA_PROJECT_URL)" "$(FIGMA_TOKEN)"

gui:
	$(BIN)/tkdesigner-gui

clean:
	$(PYTHON) -c 'from pathlib import Path; import shutil; [shutil.rmtree(path) for path in map(Path, ("build", "dist")) if path.exists()]'
