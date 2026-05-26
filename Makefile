.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: format
format:
	poetry run ruff check --select I --fix .
	poetry run ruff format .

typing:
	poetry run mypy .

.PHONY: smoke
smoke:
	poetry run yatl ./smoke

.PHONY: unit_tests
unit_tests:
	poetry run pytest

clear_env:
	poetry env remove --all 