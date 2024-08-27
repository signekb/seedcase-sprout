FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code

# poetry is installed with pip (without caching the package)
RUN pip install --no-cache-dir poetry==1.7.1

# Install dependencies first to speed up docker build (This step is cached and only
# executed when dependency files change)
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

# Copy all code to image
COPY . /code

# Create Django migrations (You may remove this when migrations are included in git)
RUN poetry run python manage.py makemigrations --no-input

# Move static assets to STATIC_ROOT
RUN poetry run python manage.py collectstatic --no-input

EXPOSE 8000

# The entrypoint executes two things:
# - "python manage.py migrate". The migrations are applied to the database
# - "gunicorn config.wsgi --bind 0.0.0.0:8000". gunicorn (application server) runs the application
ENTRYPOINT ["/bin/bash", "-c" , "poetry run python manage.py migrate && poetry run gunicorn config.wsgi --bind 0.0.0.0:8000"]
