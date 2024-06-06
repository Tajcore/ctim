# Makefile for Docker Compose-based Django operations using local.yml

# Django manage.py command shortcut
MANAGE=python manage.py

# Default make command
default: help

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "build     - Build the Docker images"
	@echo "build-django - Build the Django Docker image"
	@echo "up        - Run the Docker containers"
	@echo "up-django - Run the Django Docker container"
	@echo "down      - Stop the Docker containers"
	@echo "restart   - Restart the Docker containers"
	@echo "logs      - Follow log output of the containers"
	@echo "pre_comm  - Run the pre-commit script on staged files (without actually commiting)"
	@echo "migrate   - Apply database migrations"
	@echo "makemig   - Create new migrations based on models"
	@echo "createsu  - Create a superuser"
	@echo "shell     - Open the Django shell"
	@echo "test      - Run tests"
	@echo "startapp  - Create a new Django app"
	@echo "deploy    - Deploy to Heroku"

.PHONY: build
build:
	docker-compose -f local.yml build

.PHONY: build-django
build-django:
	docker-compose -f local.yml build django

.PHONY: up
up:
	docker-compose -f local.yml up -d

.PHONY: up-django
up-django:
	docker-compose -f local.yml up -d django

.PHONY: down
down:
	docker-compose -f local.yml down

.PHONY: restart
restart:
	docker-compose -f local.yml restart

.PHONY: logs
logs:
	docker-compose -f local.yml logs -f

.PHONY: pre_comm
pre_comm:
	# bash .git/hooks/pre-commit run --all-files
	pre-commit run --all-files

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
	docker-compose -f local.yml run --rm django $(MANAGE) test ctim.ctia.tests

.PHONY: startapp
startapp:
	@read -p "Enter the name of the new app: " appname; \
	docker-compose -f local.yml run --rm django $(MANAGE) startapp $$appname

.PHONY: openapi_schema
openapi_schema:
	docker-compose -f local.yml run --rm django $(MANAGE) spectacular --file schema.yml

.PHONY: deploy
deploy:
	@echo "You are about to deploy the current branch to Heroku."
	@read -p "Are you sure you want to continue? [y/N]: " confirm && [ $$confirm = y ] || [ $$confirm = Y ] || (echo "Deploy cancelled."; exit 1)
	@git push heroku `git rev-parse --abbrev-ref HEAD`:main
