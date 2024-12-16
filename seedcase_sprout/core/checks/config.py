from pathlib import Path

DATA_PACKAGE_SCHEMA_PATH = Path(
    "seedcase_sprout/core/checks/schemas/data-package-schema.json"
)

NAME_PATTERN = r"^[a-z0-9._-]+$"

# From https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_PATTERN = (
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0"
    r"|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>"
    r"[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
