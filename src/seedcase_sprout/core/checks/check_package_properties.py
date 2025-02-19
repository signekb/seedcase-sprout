from seedcase_sprout.core.checks.add_package_recommendations import (
    add_package_recommendations,
)
from seedcase_sprout.core.checks.check_error import CheckError
from seedcase_sprout.core.checks.check_object_against_json_schema import (
    check_object_against_json_schema,
)
from seedcase_sprout.core.checks.config import (
    DATA_PACKAGE_SCHEMA_PATH,
)
from seedcase_sprout.core.read_json import read_json


def check_package_properties(
    properties: dict, check_recommendations: bool = True
) -> list[CheckError]:
    """Checks that `properties` matches the Data Package standard (v2.0).

    Only package properties are checked. Schema constraints for resource properties are
    removed, so the internal structure of resource properties is not checked.
    Structural, type and format constraints are all checked. All schema violations are
    collected before errors are returned.

    The schema loaded or constructed in this function overrides any values specified
    in the `$schema` attribute of `properties`, including the default value.

    Args:
        properties: The package properties to check.
        check_recommendations: Whether `properties` should be checked against
            recommendations in the Data Package standard in addition to requirements.
            Defaults to True.

    Returns:
        A list of errors. An empty list, if no errors are found.
    """
    schema = read_json(DATA_PACKAGE_SCHEMA_PATH)

    # Recommendations from the Data Package standard
    if check_recommendations:
        add_package_recommendations(schema)

    # Remove schema constraints for resource properties
    schema["required"].remove("resources")
    del schema["properties"]["resources"]["minItems"]
    del schema["properties"]["resources"]["items"]

    return check_object_against_json_schema(properties, schema)
