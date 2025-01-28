from pathlib import Path

from seedcase_sprout.core.checks.check_error_matcher import CheckErrorMatcher
from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.sprout_checks.check_properties import check_properties
from seedcase_sprout.core.write_json import write_json


def write_package_properties(path: Path, properties: PackageProperties) -> Path:
    """Writes the specified package properties to the `datapackage.json` file.

    Writes a set of package properties (with or without resource properties) back to the
    `datapackage.json` file. The `path` argument is the location of the
    `datapackage.json` file. Returns the same path object as given in the `path`
    argument.

    Args:
        path: The path to the `datapackage.json` file.
        properties: The package properties to write.

    Returns:
        The path to the updated `datapackage.json` file.

    Raises:
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error for each failed check.
    """
    properties = properties.compact_dict
    check_properties(
        properties,
        ignore=[CheckErrorMatcher(validator="required", json_path=r"resources$")],
    )
    return write_json(properties, path)
