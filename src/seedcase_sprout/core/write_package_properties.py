from pathlib import Path

from seedcase_sprout.core.check_properties import check_properties
from seedcase_sprout.core.internals import _write_json
from seedcase_sprout.core.paths import PackagePath
from seedcase_sprout.core.properties import PackageProperties


def write_package_properties(
    properties: PackageProperties, path: Path | None = None
) -> Path:
    """Writes the specified package properties to the `datapackage.json` file.

    Writes a set of package properties (with or without resource properties) back to the
    `datapackage.json` file. The `path` argument is the location of the
    `datapackage.json` file. Returns the same path object as given in the `path`
    argument.

    Args:
        properties: The package properties to write. Use `PackageProperties`
            to help create the properties object.
        path: The `path` argument is to an existing `datapackage.json` file, to a
            folder that exists but is empty, or to a folder that doesn't exist yet.
            Either way, the `datapackage.json` file will be created or overwritten
            in the path given. Use `PackagePath().properties()` as a helper to get the
            correct path. If no path is provided, this function looks for the
            `datapackage.json` file in the current working directory.

    Returns:
        The path to the updated `datapackage.json` file.

    Raises:
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error for each failed check.
    """
    path = path or PackagePath().properties()
    check_properties(properties)
    return _write_json(properties.compact_dict, path)
