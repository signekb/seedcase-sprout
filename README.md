# seedcase-sprout: Grow your data in a structured and healthy way

Sprout is a component of the Seedcase ecosystem that aims to take data created or collected for research studies and "grow" it in a structured way using modern best practices for storing data.

Want to see a demo of the software? Check out our [app](https://seedcase-sprout.fly.dev/).

## Installation

This project uses Poetry to manage dependencies. To install Poetry, run:

```
pipx install poetry
```

To run any Python commands within this project, always append the command with `poetry run`, for instance:

```
poetry run python manage.py runserver
```
Or with the justfile:

```
just start-app
```
... which will run the Django project locally.


### Running the application with docker

You can run the Django application with docker:

```
# Run application
docker compose up -d

Check "http://localhost:10000"

# Terminate application
docker compose down
```

Or with the `justfile`:

```
just start-docker
just stop-docker
```

# fly.io
You can deploy to fly.io with 'flyctl'.

```bash
# Login to fly.io
flyctl auth login

# Deploy 'seedcase-sprout' based on 'fly.toml' file
flyctl deploy

# Deploy 'seedcase-sprout-preview' with
flyctl deploy --app seedcase-sprout-preview
```
