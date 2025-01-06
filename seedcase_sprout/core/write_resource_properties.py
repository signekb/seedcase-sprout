from pathlib import Path

from seedcase_sprout.core.check_data_path import check_data_path
from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.verify_package_properties import verify_package_properties
from seedcase_sprout.core.verify_resource_properties import verify_resource_properties
from seedcase_sprout.core.write_json import write_json


def write_resource_properties(path: Path, resource_properties: dict) -> Path:
    """Wrties the specified resource properties to the `datapackage.json` file.

    This functions verifies `resource_properties`, and if a
    resource with that ID is already present on the package, the properties of the
    resource with that ID are updated, with values in `resource_properties` overwriting
    preexisting values. Otherwise, `resource_properties` is added as a new resource.

    Args:
        path: The path to the `datapackage.json` file.
        resource_properties: The resource properties to add.

    Returns:
        The path to the updated `datapackage.json` file.

    Raises:
        FileNotFound: If the `datapackage.json` file doesn't exist.
        NotPropertiesError: If the resource or package properties are not correct, i.e.,
            they are incomplete or don't follow the Data Package specification.
        JSONDecodeError: If the `datapackage.json` file couldn't be read.
    """
    check_is_file(path)
    verify_resource_properties(resource_properties)

    package_properties = read_json(path)
    verify_package_properties(package_properties)

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

    Raises:
        NotPropertiesError: If the resource properties have a malformed or missing
            data path.
    """
    check_data_path(resource_properties)
    return int(Path(resource_properties["path"]).parts[1])
