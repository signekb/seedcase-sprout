@_default:
    just --list --unsorted

run-all: install-deps format-python check-python run-tests

# Generate SVG images from all PlantUML files
generate-puml-all:
  docker run --rm -v $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tsvg "**/*.puml"

# Generate SVG image from specific PlantUML file
generate-puml name:
  docker run --rm -v  $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tsvg "**/{{name}}.puml"

# Start up the docker container
start-docker:
  docker compose up -d

# Close the docker container
stop-docker:
  docker compose down

# Run tests
run-tests: install-deps
  poetry run pytest

# Check Python code with the linter for any errors that need manual attention
check-python: install-deps
  poetry run ruff check .

# Reformat Python code to match coding style and general structure
format-python: install-deps
  poetry run ruff check --fix .
  poetry run ruff format .

# Install Python package dependencies
install-deps:
  poetry install

# Add test data when running locally based on json files found in `fixtures/`
add-test-data: install-deps
  poetry run python manage.py loaddata */*/fixtures/*.json

# Reset local Sprout (remove __pycache__ folders, db, and persistent storage raw files)
reset-local:
  find . -type d -name "__pycache__" -exec rm -rf {} +
  rm db.sqlite3
  rm persistent_storage/raw/*.csv

# Build the documentation website using Quarto
build-website: install-deps
  # To let Quarto know where python is.
  export QUARTO_PYTHON=.venv/bin/python3
  poetry run quartodoc build
  poetry run quarto render --execute

check-commit:
  #!/bin/zsh
  if [[ $(git rev-parse --abbrev-ref HEAD) != "main" ]]
  then
    poetry run cz check --rev-range main..HEAD
  fi
