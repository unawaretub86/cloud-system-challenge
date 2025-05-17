# Makefile for Docker and Django commands

.PHONY: build up down restart logs shell migrate makemigrations superuser test clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make build         - Build all Docker containers"
	@echo "  make up            - Start all Docker containers"
	@echo "  make down          - Stop all Docker containers"
	@echo "  make restart       - Restart all Docker containers"
	@echo "  make logs          - View logs from all containers"
	@echo "  make shell         - Open a shell in the backend container"
	@echo "  make migrate       - Run Django migrations"
	@echo "  make makemigrations - Create new Django migrations"
	@echo "  make superuser     - Create a Django superuser"
	@echo "  make test          - Run Django tests"
	@echo "  make clean         - Remove all containers, volumes, and networks"

# Docker commands
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

shell:
	docker compose exec backend bash

# Django commands
migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

superuser:
	docker compose exec backend python manage.py createsuperuser

test:
	docker compose exec backend python manage.py test

# Clean up
clean:
	docker compose down -v --remove-orphans
