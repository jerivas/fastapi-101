pip-compile:
	python -m piptools compile --extra dev --output-file requirements.txt pyproject.toml

pip-sync:
	python -m piptools sync requirements.txt

serve:
	echo serve

build:
	echo build

lint:
	black --check .
	ruff check .

format:
	black .
	ruff check --fix .
