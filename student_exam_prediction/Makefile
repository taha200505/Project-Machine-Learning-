# Makefile
# Docker helper commands

.PHONY: help build run dev stop restart logs shell clean test push

IMAGE_NAME = student-exam-predictor
DOCKER_USERNAME = yourusername
VERSION = v1.0.0

help:
	@echo "Available commands:"
	@echo "  make build       - Build production image"
	@echo "  make build-dev   - Build development image"
	@echo "  make run         - Run production container"
	@echo "  make dev         - Run development container"
	@echo "  make stop        - Stop containers"
	@echo "  make restart     - Restart containers"
	@echo "  make logs        - View logs"
	@echo "  make shell       - Open shell in container"
	@echo "  make clean       - Remove containers and images"
	@echo "  make test        - Run tests"
	@echo "  make push        - Push to Docker Hub"

build:
	docker build -t $(IMAGE_NAME):latest -t $(IMAGE_NAME):$(VERSION) .

build-dev:
	docker build -f Dockerfile.dev -t $(IMAGE_NAME):dev .

run:
	docker-compose up -d

dev:
	docker-compose -f docker-compose.dev.yml up

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-tail:
	docker-compose logs -f --tail=100

shell:
	docker exec -it student-exam-predictor /bin/bash

shell-dev:
	docker exec -it student-exam-predictor-dev /bin/bash

clean:
	docker-compose down -v
	docker rmi $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION) || true

clean-all:
	docker-compose down -v --rmi all

test:
	docker run --rm $(IMAGE_NAME):latest pytest tests/

push: build
	docker login
	docker tag $(IMAGE_NAME):latest $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)

pull:
	docker pull $(DOCKER_USERNAME)/$(IMAGE_NAME):latest

ps:
	docker-compose ps

stats:
	docker stats student-exam-predictor

inspect:
	docker inspect student-exam-predictor

prune:
	docker system prune -af