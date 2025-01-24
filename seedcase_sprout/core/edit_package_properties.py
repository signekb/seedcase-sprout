from pathlib import Path

from frictionless.errors import PackageError

from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.verify_package_properties import (
    verify_package_properties,
)
from seedcase_sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)


def edit_package_properties(
    path: Path, properties: PackageProperties
) -> PackageProperties:
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
        The updated package properties as a Python dictionary that mimics the
            JSON structure. Use `write_package_properties()` to save it back to the
            `datapackage.json` file.

    Raises:
        FileNotFound: If the `datapackage.json` file doesn't exist.
        NotPropertiesError: If the new package properties are not correct or the current
            package properties are not well-formed.
        JSONDecodeError: If the `datapackage.json` file couldn't be read.

    Examples:
        ```{python}
        #| output: true
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package structure first
            sp.create_package_structure(path=temp_path)

            # Edit package properties
            sp.edit_package_properties(
                path=temp_path / "1" / "datapackage.json",
                properties=sp.PackageProperties(
                    title="New Package Title",
                    name="new-package-name",
                    description="New Description",
                ),
            )
        ```
    """
    properties = properties.compact_dict

    check_is_file(path)
    verify_properties_are_well_formed(properties, PackageError.type)

    current_properties = read_json(path)
    verify_properties_are_well_formed(current_properties, PackageError.type)

    current_properties.update(properties)

    verify_package_properties(current_properties)

    return PackageProperties.from_dict(current_properties)
