# Makefile for Sentiment Analysis Classifier
# Common development tasks

.PHONY: help install install-dev test test-cov lint format clean setup run-web run-api

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean build artifacts"
	@echo "  setup        - Initial project setup"
	@echo "  run-web      - Run Streamlit web app"
	@echo "  run-api      - Run FastAPI backend"

# Install production dependencies
install:
	poetry install --only main

# Install development dependencies
install-dev:
	poetry install --with dev,test

# Run tests
test:
	poetry run pytest

# Run tests with coverage
test-cov:
	poetry run pytest --cov=. --cov-report=html --cov-report=term-missing

# Run linting checks
lint:
	poetry run flake8 .
	poetry run mypy .

# Format code
format:
	poetry run black .

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Initial project setup
setup: install-dev
	@echo "Setting up development environment..."
	poetry run pre-commit install
	@echo "Development environment setup complete!"

# Run Streamlit web app
run-web:
	poetry run streamlit run apps/web/main.py

# Run FastAPI backend
run-api:
	poetry run uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

# Run both web and API (in background)
run-all: run-web run-api

# Check dependencies for security vulnerabilities
security-check:
	poetry run safety check

# Update dependencies
update-deps:
	poetry update

# Show dependency tree
deps-tree:
	poetry show --tree

# Generate requirements.txt from Poetry
export-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Run type checking only
type-check:
	poetry run mypy .

# Run formatting check only
format-check:
	poetry run black --check .

# Run all quality checks
quality: lint format-check type-check

# Install pre-commit hooks
install-hooks:
	poetry run pre-commit install

# Run pre-commit on all files
pre-commit-all:
	poetry run pre-commit run --all-files

# Create virtual environment (if not using Poetry)
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  Windows: .\\venv\\Scripts\\Activate.ps1"
	@echo "  Linux/Mac: source venv/bin/activate"

# Install with pip (alternative to Poetry)
install-pip: venv
	@echo "Installing dependencies with pip..."
	.\venv\Scripts\Activate.ps1 && pip install -r requirements.txt
	@echo "Dependencies installed with pip"

# Install dev dependencies with pip
install-dev-pip: install-pip
	@echo "Installing development dependencies with pip..."
	.\venv\Scripts\Activate.ps1 && pip install -r requirements-dev.txt
	@echo "Development dependencies installed with pip"

# Docker targets
docker-build:
	@echo "🐳 Building Docker image..."
	@./scripts/docker/build.sh

docker-run:
	@echo "🚀 Running Docker container tests..."
	@./scripts/docker/run.sh

docker-compose-up:
	@echo "📦 Starting Docker Compose services..."
	@docker-compose up -d

docker-compose-down:
	@echo "🛑 Stopping Docker Compose services..."
	@docker-compose down

docker-compose-dev:
	@echo "🔧 Starting development environment with hot-reload..."
	@docker-compose --profile dev up -d

docker-test:
	@echo "🧪 Running Docker tests..."
	@python -m pytest tests/test_docker.py -v

docker-clean:
	@echo "🧹 Cleaning up Docker resources..."
	@docker system prune -f
	@docker volume prune -f

# Combined Docker operations
docker-all: docker-build docker-run docker-test
