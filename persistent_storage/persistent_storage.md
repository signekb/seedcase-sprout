# Data folder
This folder will contain files that should remain between deployments.
The path is defined in the global variable called `PERSISTENT_STORAGE_PATH`

The folder will contain:
- The `raw` folder with unprocessed CSV files
- The SQLite file if enabled

## fly.io
We use `Fly Volumes` in fly.io to persist the files between deployments.

You can create a volume with this command:
```bash
# Create one volume in region=AMS
fly volume create persistent_storage --region ams --count 1
```

This is then referenced in fly.toml
```
...

[mounts]
  source="persistent_storage"
  destination="/code/persistent_storage"
```

WARNING: This is only possible for an fly app with one machine. Multiple
machines are not able to share a volume

## Docker Compose
In docker, we preserve the files by attaching a volume in the
docker-compose.yml. See the last lines below:

```bash
version: "3"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - persistent_storage:/code/persistent_storage
volumes:
  persistent_storage:
```
