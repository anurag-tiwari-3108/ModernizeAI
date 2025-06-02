.PHONY: install run test lint

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python3 app/frontend_gradio.py

test:
	. .venv/bin/activate && python3 -m unittest discover -s app/tests

lint:
	. .venv/bin/activate && flake8 app
