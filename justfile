set shell := ["zsh", "-cu"]

default:
    just --list

install:
    uv sync --all-extras --all-groups

test:
    uv run pytest

lint:
    uv run ruff check . --fix

types:
    uv run pyrefly check

format:
    uv run ruff format .

check: lint types format test

run-example example:
    uv run --package {{ replace(trim_end_match(example, "_example/"), "_", "-") }} python -m {{ trim_end_match(example, "_example/") }}