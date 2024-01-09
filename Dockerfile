FROM python:3.11-slim-bookworm
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=0

# poetry is installed with pip (without caching the package)
RUN pip install --no-cache-dir poetry==1.7.1

# Install dependencies first to speed up docker build (This step is cached and only
# executed when dependecy files change)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-cache --no-interaction --no-root

# Copy all code to image
COPY . .
EXPOSE 10000

ENTRYPOINT ["/bin/bash", "-c" , "poetry run python manage.py migrate && poetry run gunicorn seedcase_sprout.wsgi --bind 0.0.0.0:10000"]
