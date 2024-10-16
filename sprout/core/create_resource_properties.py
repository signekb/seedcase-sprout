from pathlib import Path

from frictionless.errors import ResourceError

from sprout.core.create_relative_resource_data_path import (
    create_relative_resource_data_path,
)
from sprout.core.edit_property_field import edit_property_field
from sprout.core.verify_is_dir import verify_is_dir
from sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)


def create_resource_properties(path: Path, properties: dict) -> dict:
    """Creates a valid properties object for the specified resource.

    This function sets up and structures a new resource property by taking
    the fields given in the `properties` argument to fill them and prepare
    them to be added to the `datapackage.json` file.

    Args:
        path: the path to the resource `id` folder; use `path_resource()`
            to provide the correct path or use the output of
            `create_resource_structure()`.
        properties: the properties of the resource; must be given as a
            JSON object following the Data Package specification; use
            the `ResourceProperties` class to provide the correct fields.
            See the `ResourceProperties` help documentation for details
            on what can or needs to be filled in.

    Raises:
        NotADirectoryError: if path does not point to a directory.
        NotPropertiesError: if properties are not correct Frictionless
            resource properties.

    Returns:
        the properties object, verified and updated
    """
    verify_is_dir(path)
    verify_properties_are_well_formed(properties, ResourceError.type)
    data_path = create_relative_resource_data_path(path)
    return edit_property_field(properties, "path", str(data_path))
