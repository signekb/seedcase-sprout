from pathlib import Path

from frictionless.errors import PackageError

from sprout.core.read_json import read_json
from sprout.core.verify_is_file import verify_is_file
from sprout.core.verify_package_properties import (
    verify_package_properties,
)
from sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)


def edit_package_properties(path: Path, properties: dict) -> dict:
    """Edits the properties of an existing package.

    Use this any time you want to edit the package's properties and particularly
    after using `create_package_structure()`. Because
    `create_package_structure()` also creates an empty `datapackage.json` file,
    `edit_package_properties()` is used to fill in the properties file with
    details specific for the package.

    When you need to edit the `datapackage.json` properties, use this function
    to ensure the properties are correctly structured and written. It only
    edits the properties of the package itself, not on the data resources contained
    within the package.

    If the values in `properties` are well-formed, they will overwrite any preexisting
    values within the original package properties.

    Args:
        path: The path to the `datapackage.json` file. Use `path_package_properties()`
            to provide the correct path.
        properties: The new package properties to update from the original. Use
            `PackageProperties` to provide a correctly structured properties
            dictionary. See `help(PackageProperties)` for details on how to use it.

    Returns:
        The updated package properties as a Python dictionary that mimicks the
        JSON structure. Use `write_package_properties()` to save it back to the
        `datapackage.json` file.

    Raises:
        FileNotFound: If the `datapackage.json` file doesn't exist.
        NotPropertiesError: If the new package properties are not correct or the current
            package properties are not well-formed.
        JSONDecodeError: If the `datapackage.json` file couldn't be read.
    """
    verify_is_file(path)
    verify_properties_are_well_formed(properties, PackageError.type)

    current_properties = read_json(path)
    verify_properties_are_well_formed(current_properties, PackageError.type)

    current_properties.update(properties)

    return verify_package_properties(current_properties)
