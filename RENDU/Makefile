NAME=a_maze_ing.py
TEST=print_term.py
CONFIG=config.txt

all: ${TEST}

install:
	pip install pydantic colorama type-colorama flake8 mypy

run:
	python3 ${TEST} ${CONFIG}

debug:
	python3 -m pdb ${TEST} ${CONFIG}

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

.PHONY: install run debug clean lint lint-strict
