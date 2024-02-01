@_default:
    just --list --unsorted

# Generate PNG images from all PlantUML files
generate-puml-all:
  docker run --rm -v $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tpng "**/*.puml"

# Generate PNG image from specific PlantUML file
generate-puml name:
  docker run --rm -v  $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tpng "**/{{name}}.puml"

# Start up the docker container
start-docker:
  docker compose up -d

# Close the docker container
stop-docker:
  docker compose down

# Create and apply migration files
update-migrations:
  poetry run python manage.py makemigrations
  poetry run python manage.py migrate

# Run Django tests
run-tests:
  poetry run python manage.py test

# Check Python code with the linter for any errors that need manual attention
check-python:
  poetry run ruff check .

# Reformat Python code to match coding style and general structure
format-python:
  poetry run ruff check --fix .
  poetry run ruff format .

# Builds and starts a development web server for the Django app (at http://localhost:8000)
start-app:
  poetry run python ./manage.py runserver
  # Not sure if this works for others?
  # xdg-open http://localhost:8000

# Install Python packagee dependencies
install-deps:
  # no-root to not install the parent folder as a package
  poetry install --no-root

# Add test data when running locally based on app/fixtures/sample.json
add-test-data:
  just update-migrations
  poetry run python manage.py loaddata sample
