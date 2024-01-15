FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code

# poetry is installed with pip (without caching the package)
RUN pip install --no-cache-dir poetry

# Install dependencies first to speed up docker build (This step is cached and only
# executed when dependecy files change)
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

# Copy all code to image
COPY . /code

EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "seedcase_sprout.wsgi"]
ENTRYPOINT ["/bin/bash", "-c" , "poetry run python manage.py migrate && poetry run gunicorn seedcase_sprout.wsgi --bind 0.0.0.0:8000"]
