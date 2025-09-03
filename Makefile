.PHONY: help install test lint format run docker-build docker-up docker-down clean

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias del proyecto
	pip install -r requirements.txt
	pip install -e .

install-dev: ## Instala dependencias de desarrollo
	pip install -r requirements.txt
	pip install -e ".[dev]"

test: ## Ejecuta los tests
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit: ## Ejecuta solo tests unitarios
	pytest tests/unit/ -v

lint: ## Ejecuta linting del código
	flake8 src tests
	mypy src

format: ## Formatea el código
	black src tests
	isort src tests

format-check: ## Verifica el formato del código
	black --check src tests
	isort --check-only src tests

run: ## Ejecuta la aplicación localmente
	uvicorn src.marketing_afiliados.main:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Construye la imagen Docker
	docker-compose build

docker-up: ## Levanta los servicios con Docker Compose
	docker-compose up -d

docker-down: ## Detiene los servicios Docker
	docker-compose down

docker-logs: ## Muestra los logs de los servicios
	docker-compose logs -f

clean: ## Limpia archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

setup-env: ## Configura el archivo de entorno
	cp env.example .env
	@echo "Archivo .env creado. Edítalo con tus configuraciones."

migrate: ## Ejecuta migraciones de base de datos (placeholder)
	@echo "Migraciones no implementadas aún"

seed: ## Ejecuta seeders de base de datos (placeholder)
	@echo "Seeders no implementados aún"

check: format-check lint test ## Ejecuta todas las verificaciones

ci: install-dev check ## Pipeline de CI completo
