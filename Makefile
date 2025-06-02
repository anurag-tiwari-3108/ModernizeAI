.PHONY: install run test

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python3 frontend_gradio.py

test:
	. .venv/bin/activate && python3 -m unittest test_agent_pipeline.py
