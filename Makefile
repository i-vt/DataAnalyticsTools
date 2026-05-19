.PHONY: install dev test lint typecheck coverage clean docker-build docker-test docker-run

# ── Local development ───────────────────────────

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check src/ tests/

typecheck:
	mypy src/

coverage:
	pytest --cov=data_analytics_tools --cov-report=term-missing --cov-report=html

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

# ── Docker ──────────────────────────────────────

docker-build:
	docker build -t data-analytics-tools .

docker-test:
	docker compose run --rm test

docker-run:
	docker compose run --rm app $(CMD)
