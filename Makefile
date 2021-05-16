.PHONY: build, clean, test, local-all, sync-datadog, local-up, local-down

# Variables
APP_DIR = test/app
TERRAFORM_DIR = test/terraform
DOCKER_COMPOSE_FILE = $(APP_DIR)/docker-compose.yml


# *** Main targets

# Build
build: clean
	python3 -m build

clean:
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build

# Deploy datadog configs and standup local
local-all: sync-datadog local-up

# Build and deploy test app locally along with associated DataDog monitors
# - Datadog account env vars must be specified
local-up: docker local-down
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

local-down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

test: gen-tf

# Deploy datadog configs
sync-datadog: gen-tf
	terraform -chdir=$(TERRAFORM_DIR) apply


# *** Supporting targets

gen-tf:
	python monitor-generator/generator/main.py $(APP_DIR)/app:app $(TERRAFORM_DIR)/auto-gen-monitors/ test

# Build all docker assets
docker:
	docker-compose -f $(DOCKER_COMPOSE_FILE) build
	docker image prune -f
