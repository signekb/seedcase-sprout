@_default:
    just --list --unsorted

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

# Update the Django migration files
update-migrations: install-deps
  yes | poetry run python manage.py makemigrations
  poetry run python manage.py migrate

# Run Django tests
run-tests: install-deps update-migrations
  poetry run pytest

# Check Python code with the linter for any errors that need manual attention
check-python: install-deps
  poetry run ruff check .

# Reformat Python code to match coding style and general structure
format-python: install-deps
  poetry run ruff check --fix .
  poetry run ruff format .

# Builds and starts a development web server for the Django app (at http://localhost:8000)
start-app: install-deps update-migrations
  poetry run python ./manage.py runserver

# Install Python package dependencies
install-deps:
  poetry install

# Add test data when running locally based on json files found in `fixtures/`
add-test-data: install-deps update-migrations
  poetry run python manage.py loaddata */*/fixtures/*.json

# Reset local Sprout (remove __pycache__ folders, db, migrations, and persistent storage raw files)
reset-local: 
  find . -type d -name "__pycache__" -exec rm -rf {} +
  find */**/migrations -type f ! -name '__init__.py' -exec rm {} \;
  rm db.sqlite3
  rm persistent_storage/raw/*.csv

# Build the documentation website using Quarto
build-website:
  docker run --rm -v $(pwd):/site -w /site ghcr.io/quarto-dev/quarto:latest quarto render

# Add files for a new function (function file and test file)
add-function app part name:
  touch ./{{app}}/{{part}}/{{name}}.py
  touch ./tests/{{part}}/test_{{name}}.py
