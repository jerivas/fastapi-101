pip-compile:
	python -m piptools compile --extra dev --output-file requirements.txt pyproject.toml

pip-sync:
	python -m piptools sync requirements.txt

dev:
	uvicorn app.main:app --host 0.0.0.0 --reload --port 9000

serve:
	uvicorn app.main:app --host 0.0.0.0

lint:
	black --check .
	ruff check .

format:
	black .
	ruff check --fix .
