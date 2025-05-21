from pathlib import Path

from seedcase_sprout.core.check_properties import (
    check_properties,
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
    resource with that name is already present on the package, the properties of that
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
                )
            )
        ```
    """
    path = path or PackagePath().properties()
    _check_is_file(path)
    check_resource_properties(resource_properties)

    package_properties = _read_json(path)
    check_properties(PackageProperties().from_dict(package_properties))

    resource_properties = resource_properties.compact_dict
    current_resource = next(
        (
            resource
            for resource in package_properties.get("resources", [])
            if resource["name"] == resource_properties["name"]
        ),
        None,
    )
    if current_resource:
        updated_properties = nested_update(current_resource, resource_properties)
        current_resource.clear()
        current_resource.update(updated_properties)
    else:
        resources = package_properties.get("resources", [])
        package_properties["resources"] = resources + [resource_properties]

    return _write_json(package_properties, path)
