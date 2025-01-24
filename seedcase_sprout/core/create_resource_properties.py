from pathlib import Path

from frictionless.errors import ResourceError

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.create_relative_resource_data_path import (
    create_relative_resource_data_path,
)
from seedcase_sprout.core.edit_property_field import edit_property_field
from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)


def create_resource_properties(
    path: Path, properties: ResourceProperties
) -> ResourceProperties:
    """Creates a valid properties object for the specified resource.

    This function sets up and structures a new resource property by taking
    the fields given in the `properties` argument to fill them and prepare
    them to be added to the `datapackage.json` file.

    Args:
        path: The path to the resource `id` folder; use `path_resource()`
            to provide the correct path or use the output of
            `create_resource_structure()`.
        properties: The properties of the resource; must be given as a
            JSON object following the Data Package specification; use
            the `ResourceProperties` class to provide the correct fields.
            See the `ResourceProperties` help documentation for details
            on what can or needs to be filled in.

    Returns:
        The properties object, verified and updated

    Raises:
        NotADirectoryError: If path does not point to a directory.
        NotPropertiesError: If properties are not correct Frictionless
            resource properties.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package and resource structure first
            sp.create_package_structure(path=temp_path)
            sp.create_resource_structure(path=temp_path / "1" / "resources")

            # Create resource properties
            sp.create_resource_properties(
                path=temp_path / "1" / "resources" / "1",
                properties=sp.ResourceProperties(
                    name="new-resource-name",
                    path="data.parquet",
                ),
            )
        ```
    """
    properties = properties.compact_dict
    check_is_dir(path)
    verify_properties_are_well_formed(properties, ResourceError.type)
    data_path = create_relative_resource_data_path(path)
    edited_properties = edit_property_field(properties, "path", str(data_path))

    return ResourceProperties.from_dict(edited_properties)
