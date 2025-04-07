from pathlib import Path

from seedcase_sprout.core.check_datapackage import CheckErrorMatcher
from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.sprout_checks.check_properties import check_properties
from seedcase_sprout.core.sprout_checks.check_resource_properties import (
    check_resource_properties,
)
from seedcase_sprout.core.write_json import write_json


def write_resource_properties(
    path: Path, resource_properties: ResourceProperties
) -> Path:
    """Writes the specified resource properties to the `datapackage.json` file.

    This functions verifies `resource_properties`, and if a
    resource with that ID is already present on the package, the properties of that
    resource are updated. The values in `resource_properties` overwrite
    preexisting values. Otherwise, `resource_properties` is added as a new resource.


    Args:
        path: The path to the `datapackage.json` file. Use `PackagePath().properties()`
            to help give the correct path.
        resource_properties: The resource properties to add. Use
            `ResourceProperties` to help create this object.

    Returns:
        The path to the updated `datapackage.json` file.

    Raises:
        FileNotFound: If the `datapackage.json` file doesn't exist.
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error per failed check.
        JSONDecodeError: If the `datapackage.json` file couldn't be read.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        temp_dir = Path(tempfile.TemporaryDirectory().name)
        temp_dir.mkdir()

        # Create package and resource structure first
        sp.write_package_properties(
            properties=sp.example_package_properties(),
            path=sp.PackagePath(temp_dir).properties()
        )

        # TODO: Write package properties that passes checks
        # sp.create_resource_structure(path=sp.PackagePath(temp_dir).resource("1")
        # Write package properties
        # sp.write_package_properties(
        #     path=temp_dir / "1" / "datapackage.json",
        #     package_properties=sp.PackageProperties(
        #         title="New Package Title",
        #         name="new-package-name",
        #         description="New Description",
        #     ),

        # Write resource properties
        # sp.write_resource_properties(
        #     path=temp_dir / "1" / "datapackage.json",
        #     resource_properties=sp.ResourceProperties(
        #         name="new-resource-name",
        #         title="New resource name",
        #         description="This is a new resource",
        #         path="data.parquet",
        #     ),
        # )
        ```
    """
    check_is_file(path)
    check_resource_properties(resource_properties)

    package_properties = read_json(path)
    check_properties(
        package_properties,
        ignore=[CheckErrorMatcher(validator="required", json_path="resources")],
    )

    resource_properties = resource_properties.compact_dict
    resource_id = get_resource_id_from_properties(resource_properties)
    current_resource = get_resource_properties(package_properties, resource_id)
    if current_resource:
        current_resource.update(resource_properties)
    else:
        package_properties["resources"].append(resource_properties)

    return write_json(package_properties, path)


def get_resource_properties(package_properties: dict, resource_id: int) -> dict | None:
    """Finds the resource properties with the given ID within the given package.

    Args:
        package_properties: The package properties with the resources to look through.
        resource_id: The ID of the resource to find.

    Returns:
        The resource with the specified ID, if found. Otherwise returns `None`.
    """
    for resource in package_properties["resources"]:
        if get_resource_id_from_properties(resource) == resource_id:
            return resource


def get_resource_id_from_properties(resource_properties: dict) -> int:
    """Returns the resource ID of the specified resource properties.

    Args:
        resource_properties: The resource properties object.

    Returns:
        The ID of the resource.
    """
    return int(Path(resource_properties["path"]).parts[1])
