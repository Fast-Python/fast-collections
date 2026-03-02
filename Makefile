.PHONY: all build develop test fmt lint clean clean-cargo check
UV ?= uv

all: develop

fmt:
	cargo fmt

test-cargo:
	cargo fmt --all -- --check
	cargo clippy -- -D warnings
	cargo build --release
	cargo test --release

format:
	$(UV) run ruff format
	$(UV) run ruff check

lint:
	$(UV) run ruff check --exit-non-zero-on-fix
	$(UV) run ruff format --check --diff

build:
	$(UV) run maturin build --release

develop:
	$(UV) run maturin develop --release

unit:
	$(UV) run pytest 

clean-cargo:
	cargo clean

clean: clean-cargo
	rm -rf target/wheels


test: build unit check