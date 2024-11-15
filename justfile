@_default:
    just --list --unsorted

# Run all the build recipes
run-all: reset-local install-deps format-python check-python test-python check-commits build-website

# Install Python package dependencies
install-deps:
  poetry install

# Generate SVG images from all PlantUML files
generate-puml-all:
  docker run --rm -v $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tsvg "**/*.puml"

# Generate SVG image from specific PlantUML file
generate-puml name:
  docker run --rm -v  $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tsvg "**/{{name}}.puml"

# Run the Python tests
test-python:
  poetry run pytest

# Check Python code with the linter for any errors that need manual attention
check-python:
  poetry run ruff check .

# Reformat Python code to match coding style and general structure
format-python:
  poetry run ruff check --fix .
  poetry run ruff format .

# Reset local Sprout (remove __pycache__ folders, generated build files, etc)
reset-local:
  find . -type d -name "__pycache__" -exec rm -rf {} +
  rm -rf .storage

# Build the documentation website using Quarto
build-website:
  # To let Quarto know where python is.
  export QUARTO_PYTHON=.venv/bin/python3
  poetry run quartodoc build
  poetry run quarto render --execute

# Run checks on commits with non-main branches
check-commits:
  #!/bin/zsh
  if [[ $(git rev-parse --abbrev-ref HEAD) != "main" ]]
  then
    poetry run cz check --rev-range main..HEAD
  fi
