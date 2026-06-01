NAME=a_maze_ing.py
CONFIG=config.txt

all: ${NAME}

install:
	pip install poetry
	python3 -m poetry install --no-root

run:
	python3 ${NAME} ${CONFIG}

debug:
	python3 -m pdb ${NAME} ${CONFIG}

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf maze.txt

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

.PHONY: install run debug clean lint lint-strict
