.PHONY: setup train run_server run_client test

setup:
	pip install -r requirements.txt

train:
	python models/FHEModel.py

run_server:
	uvicorn src.server.server:app --host 0.0.0.0 --port 8000

run_client:
	uvicorn src.client.client:app --host 127.0.0.1 --port 8001

test:
	PYTHONPATH=. pytest tests/test_api.py
