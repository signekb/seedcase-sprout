from pathlib import Path

from seedcase_sprout.core.check_properties import (
    check_package_properties,
    check_resource_properties,
)
from seedcase_sprout.core.internals import _check_is_file, _read_json, _write_json
from seedcase_sprout.core.nested_update import nested_update
from seedcase_sprout.core.paths import PackagePath
from seedcase_sprout.core.properties import PackageProperties, ResourceProperties


def write_resource_properties(
    resource_properties: ResourceProperties, path: Path | None = None
) -> Path:
    """Writes the specified resource properties to the `datapackage.json` file.

    This functions verifies `resource_properties`, and if a
    resource with that ID is already present on the package, the properties of that
    resource are updated. The values in `resource_properties` overwrite
    preexisting values. Otherwise, `resource_properties` is added as a new resource.


    Args:
        resource_properties: The resource properties to add. Use
            `ResourceProperties` to help create this object.
        path: The path to the `datapackage.json` file. Use `PackagePath().properties()`
            to help give the correct path. If no path is provided, this function looks
            for the `datapackage.json` file in the current working directory.

    Returns:
        The path to the updated `datapackage.json` file.

    Raises:
        FileNotFound: If the `datapackage.json` file doesn't exist.
        ExceptionGroup: If there is an error in the properties. A group of
            `CheckError`s, one error per failed check.
        JSONDecodeError: If the `datapackage.json` file couldn't be read.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp

        with sp.ExamplePackage():
            sp.write_resource_properties(
                resource_properties=sp.ResourceProperties(
                    name="new-resource-name",
                    title="New resource name",
                    description="This is a new resource",
                    path="resources/2/data.parquet",
                )
            )
        ```
    """
    path = path or PackagePath().properties()
    _check_is_file(path)
    check_resource_properties(resource_properties)

    package_properties = _read_json(path)
    check_package_properties(PackageProperties().from_dict(package_properties))

    resource_properties = resource_properties.compact_dict
    resource_id = get_resource_id_from_properties(resource_properties)
    current_resource = get_resource_properties(package_properties, resource_id)
    if current_resource:
        updated_properties = nested_update(current_resource, resource_properties)
        current_resource.clear()
        current_resource.update(updated_properties)
    else:
        resources = package_properties.get("resources", [])
        package_properties["resources"] = resources + [resource_properties]

    return _write_json(package_properties, path)


def get_resource_properties(package_properties: dict, resource_id: int) -> dict | None:
    """Finds the resource properties with the given ID within the given package.

    Args:
        package_properties: The package properties with the resources to look through.
        resource_id: The ID of the resource to find.

    Returns:
        The resource with the specified ID, if found. Otherwise returns `None`.
    """
    for resource in package_properties.get("resources", []):
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
