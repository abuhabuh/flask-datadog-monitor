.PHONY: build check clean test local-all sync-datadog local-up local-down

# Variables
APP_DIR = test/app
TERRAFORM_DIR = test/terraform
DOCKER_COMPOSE_FILE = $(APP_DIR)/docker-compose.yml
PYTHON_EXEC = export PYTHONPATH=`pwd` && venv/bin/python


# *** Main targets

# Build
build: clean
	python3 -m build
# Clean assets from previous build process
clean: clean-py-cache
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

check: clean-py-cache
	mypy -p flask_datadog
test:
	@echo ">>>"
	@echo ">>> Running unit tests with pytest"
	@echo ">>>"
	pytest .
	@echo ">>>"
	@echo ">>> Running custom integration test script"
	@echo ">>>"
	$(PYTHON_EXEC) test/integration/tf_output_generation_test.py
	@echo ">>>"
	@echo ">>> Test completes"
	@echo ">>>"

# Deploy datadog configs
sync-datadog: gen-tf
	terraform -chdir=$(TERRAFORM_DIR) apply


# *** Supporting targets

clean-py-cache:
	find . | grep -E "(__pycache__|.mypy_cache|\.pyc|\.pyo$$)" | xargs rm -rf

# Build all docker assets
docker:
	docker-compose -f $(DOCKER_COMPOSE_FILE) build
	docker image prune -f

gen-tf:
	$(PYTHON_EXEC) flask_datadog/generator/main.py $(APP_DIR)/app:app $(TERRAFORM_DIR)/auto-gen-monitors test
