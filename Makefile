PYTHON = python3
.PHONY = test

test:
	PYTHONPATH=. ${PYTHON} -m pytest

game1:
	${PYTHON} src/main.py rock

game4:
	${PYTHON} src/main.py rock paper scissors 4

game3:
	${PYTHON} src/main.py rock paper scissors

game7:
	${PYTHON} src/main.py python rust ruby java php js c# 

format:
	ruff format .

lint:
	ruff check .