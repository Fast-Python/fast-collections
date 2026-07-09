.DEFAULT_GOAL := help

.PHONY: help
help: ## Show the help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run linting checks
	poetry run ruff check .

.PHONY: format
format: ## Format code with ruff
	poetry run ruff check --select I --fix .
	poetry run ruff format .

typing:  ## Run typing checks
	poetry run mypy .

.PHONY: smoke
smoke: ## Run E2E checks
	poetry run yatl ./smoke

.PHONY: unit_tests
unit_tests: ## Run unit tests with pytest
	poetry run pytest
