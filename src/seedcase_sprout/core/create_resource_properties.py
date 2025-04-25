from pathlib import Path

from seedcase_sprout.core.check_properties import (
    check_resource_properties,
)
from seedcase_sprout.core.create_relative_resource_data_path import (
    create_relative_resource_data_path,
)
from seedcase_sprout.core.internals import _check_is_dir
from seedcase_sprout.core.paths import PackagePath
from seedcase_sprout.core.properties import ResourceProperties


def create_resource_properties(
    properties: ResourceProperties, path: Path | None = None
) -> ResourceProperties:
    """Creates a valid properties object for the specified resource.

    This function sets up and structures a new resource property by taking
    the fields given in the `properties` argument to fill them and prepare
    them to be added to the `datapackage.json` file.

    Args:
        properties: The properties of the resource; must be given as a
            `ResourceProperties` object following the Data Package specification.
            See the `ResourceProperties` help documentation for details
            on what can or needs to be filled in.
        path: The path to the resource `id` folder; use `PackagePath().resource()`
            to provide the correct path.

    Returns:
        The properties object, verified and updated.

    Raises:
        NotADirectoryError: If path does not point to a directory.
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error per failed check.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp

        with sp.ExamplePackage():
            resource_properties = sp.example_resource_properties()
            # TODO: do not have to change name after data path is refactored to use name
            resource_properties.name = "1"
            sp.create_resource_properties(properties=resource_properties)
        ```
    """
    path = path or PackagePath().resource(properties.name)
    _check_is_dir(path)
    properties.path = str(create_relative_resource_data_path(path))
    return check_resource_properties(properties)
