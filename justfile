@_default:
    just --list --unsorted

# Run all build-related recipes in the justfile
run-all: install-deps format-python check-python test-python check-commits build-website

# Install Python package dependencies
install-deps:
  poetry sync

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

# Build the documentation website using Quarto
build-website:
  # To let Quarto know where python is.
  export QUARTO_PYTHON=.venv/bin/python3
  poetry run quartodoc build
  poetry run quarto render --execute

# Run checks on commits with non-main branches
check-commits:
  #!/bin/zsh
  branch_name=$(git rev-parse --abbrev-ref HEAD)
  number_of_commits=$(git rev-list --count HEAD ^$branch_name)
  if [[ ${branch_name} != "main" && ${number_of_commits} -gt 0 ]]
  then
    poetry run cz check --rev-range main..HEAD
  else
    echo "Not on main or haven't committed yet."
  fi
