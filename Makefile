.PHONY: run test build rebuild lint

run:
	pipenv run uvicorn app.main:app --reload

test:
	pipenv run pytest

build:
	docker build -t userstransactions .

rebuild:
	@echo "Clear .pyc"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Clear pipenv"
	-pipenv --rm || true
	@echo "Clear pipfile.lock"
	rm -f Pipfile.lock
	@echo "Clear cache"
	rm -rf .pytest_cache
	@echo "Install"
	pipenv install --dev

lint:
	@echo "flake8"
	pipenv run flake8 .
	@echo "Check black"
	pipenv run black --check .
	@echo "isort"
	pipenv run isort --check-only .
	@echo "mypy"
	pipenv run mypy .
