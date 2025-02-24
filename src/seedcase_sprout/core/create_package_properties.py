from pathlib import Path
from uuid import uuid4

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.create_properties_path import create_properties_path
from seedcase_sprout.core.get_iso_timestamp import get_iso_timestamp
from seedcase_sprout.core.properties import PackageProperties
from seedcase_sprout.core.sprout_checks.check_package_properties import (
    check_package_properties,
)
from seedcase_sprout.core.write_json import write_json


def create_package_properties(
    properties: PackageProperties, path: Path = Path.cwd()
) -> list[Path]:
    """Creates a new `datapackage.json` file with properties for a new package.

    This is the first function to use to create a new data package. It creates a
    `datapackage.json` file based on the values you give it with the `properties`
    argument. You can use the `PackageProperties` class to help create a valid
    properties object that has the correct fields.

    By default, the function will add the `id`, `version`, and `created` fields to the
    properties object. See the `PackageProperties` class documentation for more
    information.

    Args:
        properties: A `PackageProperties` object containing the properties for the
            package.
        path: The path to the folder where the data package will be created.
            Defaults to the working directory.

    Returns:
        The path to the `datapackage.json` file in the created folder.

    Raises:
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error per failed check.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create package properties
            sp.create_package_properties(
                # Using a built-in example properties object
                properties=sp.example_package_properties(),
                path=temp_path
            )
        ```
    """
    # The path should already exist as a directory.
    check_is_dir(path)
    properties.id = properties.id or str(uuid4())
    properties.version = properties.version or "0.1.0"
    properties.created = properties.created or get_iso_timestamp()
    check_package_properties(
        properties,
    )
    # Creates a path to the properties files.
    properties_path = create_properties_path(path)
    return write_json(properties.compact_dict, properties_path)
