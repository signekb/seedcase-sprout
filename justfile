@_default:
    just --list --unsorted

# Generate PNG images from PlantUML files
generate-puml:
  docker run --rm -v $(pwd):/puml -w /puml ghcr.io/plantuml/plantuml:latest -tpng "**/*.puml"

# Start up the docker container
start-docker:
  docker compose up -d

# Close the docker container
stop-docker:
  docker compose down

# Update the Django migration files
update-migrations:
  poetry run python manage.py makemigrations

run-tests:
  poetry run python manage.py test

# Run Python linter to check for any errors in the code
lint-python:
  poetry run ruff check --fix .

# Reformat Python code to match coding style and general structure
format-python:
  poetry run ruff format .

# Builds and starts a development web server for the Django app (at http://localhost:8000)
start-app:
  poetry run python ./manage.py runserver
  # Not sure if this works for others?
  # xdg-open http://localhost:8000
