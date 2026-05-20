.PHONY: install uninstall run debug clean lint lint-strict

install: requirements.txt
	/bin/bash -c "python3 -m virtualenv mazing && source mazing/bin/activate && pip install -r requirements.txt"
	

run:
	/bin/bash -c "source mazing/bin/activate && python3 a_maze_ing.py config.txt && deactivate"

debug:
	/bin/bash -c "source mazing/bin/activate && python3 -m pdb a_maze_ing.py config.txt && deactivate"

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf maze_generator/__pycache__
	rm -rf maze.txt

uninstall: clean
	rm -rf mazing

lint:
	/bin/bash -c "source mazing/bin/activate && python3 -m flake8 --exclude=mazing . \
	&& python3 -m mypy --exclude mazing . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs \
	&& deactivate"

lint-strict:
	/bin/bash -c "source mazing/bin/activate && python3 -m flake8 --exclude=mazing . \
	&& python3 -m mypy --strict --exclude mazing . && deactivate"
