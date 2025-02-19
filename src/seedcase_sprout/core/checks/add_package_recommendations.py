from seedcase_sprout.core.checks.config import NAME_PATTERN, SEMVER_PATTERN
from seedcase_sprout.core.checks.required_fields import (
    PACKAGE_RECOMMENDED_FIELDS,
)


def add_package_recommendations(schema: dict) -> dict:
    """Add recommendations from the Data Package standard to the schema.

    Modifies the schema in place.

    Args:
        schema: The full Data Package schema.

    Returns:
        The updated Data Package schema.
    """
    schema["required"].extend(PACKAGE_RECOMMENDED_FIELDS.keys())
    schema["properties"]["name"]["pattern"] = NAME_PATTERN
    schema["properties"]["version"]["pattern"] = SEMVER_PATTERN
    schema["properties"]["contributors"]["items"]["required"] = ["title"]
    schema["properties"]["sources"]["items"]["required"] = ["title"]
    return schema
