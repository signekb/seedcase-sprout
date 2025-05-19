@_default:
    just --list --unsorted

# Run all build-related recipes in the justfile
run-all: install-deps format-python check-python test-python check-security check-spelling check-commits build-website check-unused

# Install Python package dependencies
install-deps:
  uv sync --all-extras --dev

# Run the Python tests
test-python:
  uv run pytest
  # Make the badge from the coverage report
  uv run genbadge coverage \
    -i coverage.xml \
    -o htmlcov/coverage.svg

# Check Python code with the linter for any errors that need manual attention
check-python:
  uv run ruff check .

# Reformat Python code to match coding style and general structure
format-python:
  uv run ruff check --fix .
  uv run ruff format .

# Build the documentation website using Quarto
build-website:
  # To let Quarto know where python is.
  export QUARTO_PYTHON=.venv/bin/python3
  # Delete any previously built files from quartodoc.
  # -f is to not give an error if the files don't exist yet.
  rm -f docs/reference/*.qmd
  uv run quartodoc build
  uv run quarto render --execute

# Build the documentation as PDF using Quarto
build-pdf:
  # To let Quarto know where python is.
  export QUARTO_PYTHON=.venv/bin/python3
  uv run quarto install tinytex
  # For generating images from Mermaid diagrams
  uv run quarto install chromium
  uv run quarto render --profile pdf --to pdf
  find docs -name "mermaid-figure-*.png" -delete


# Run checks on commits with non-main branches
check-commits:
  #!/bin/zsh
  branch_name=$(git rev-parse --abbrev-ref HEAD)
  number_of_commits=$(git rev-list --count HEAD ^main)
  if [[ ${branch_name} != "main" && ${number_of_commits} -gt 0 ]]
  then
    uv run cz check --rev-range main..HEAD
  else
    echo "Can't either be on ${branch_name} or have more than ${number_of_commits}."
  fi

# Run basic security checks on the package
check-security:
  uv run bandit -r src/

# Check for spelling errors in files
check-spelling:
  uv run typos

# Check for unused code in the package and its tests
check-unused:
  # exit code=0: No unused code was found
  # exit code=3: Unused code was found
  # Three confidence values:
  # - 100 %: function/method/class argument, unreachable code
  # - 90 %: import
  # - 60 %: attribute, class, function, method, property, variable
  vulture src/ tests/
