# Makefile for Docker Compose-based Django operations using local.yml

# Django manage.py command shortcut
MANAGE=python manage.py

# Default make command
default: help

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "build     - Build the Docker images"
	@echo "up        - Run the Docker containers"
	@echo "down      - Stop the Docker containers"
	@echo "restart   - Restart the Docker containers"
	@echo "logs      - Follow log output of the containers"
	@echo "migrate   - Apply database migrations"
	@echo "makemig   - Create new migrations based on models"
	@echo "createsu  - Create a superuser"
	@echo "shell     - Open the Django shell"
	@echo "test      - Run tests"
	@echo "startapp  - Create a new Django app"
	@echo "openapi_schema   - Create a new schema.yml"

.PHONY: build
build:
	docker-compose -f local.yml build

.PHONY: up
up:
	docker-compose -f local.yml up -d

.PHONY: down
down:
	docker-compose -f local.yml down

.PHONY: restart
restart:
	docker-compose -f local.yml restart

.PHONY: logs
logs:
	docker-compose -f local.yml logs -f

.PHONY: migrate
migrate:
	docker-compose -f local.yml run --rm django $(MANAGE) migrate

.PHONY: makemig
makemig:
	docker-compose -f local.yml run --rm django $(MANAGE) makemigrations

.PHONY: createsu
createsu:
	docker-compose -f local.yml run --rm django $(MANAGE) createsuperuser

.PHONY: shell
shell:
	docker-compose -f local.yml run --rm django $(MANAGE) shell

.PHONY: test
test:
	docker-compose -f local.yml run --rm django $(MANAGE) test

.PHONY: startapp
startapp:
	@read -p "Enter the name of the new app: " appname; \
	docker-compose -f local.yml run --rm django $(MANAGE) startapp $$appname

.PHONY: openapi_schema
openapi_schema:
	docker-compose -f local.yml run --rm django $(MANAGE) spectacular --file schema.yml