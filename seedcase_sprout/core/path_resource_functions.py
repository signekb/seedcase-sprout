from pathlib import Path

from seedcase_sprout.core import path_package
from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.check_is_resource_dir import check_is_resource_dir


def path_resource(package_id: int, resource_id: int) -> Path:
    """Gets the absolute path to the specified resource.

    Args:
        package_id: The ID of the package.
        resource_id: The ID of the resource.

    Returns:
        The absolute path to the specified resource.
    """
    path = path_resources(package_id) / str(resource_id)
    return check_is_resource_dir(path)


def path_resource_data(package_id: int, resource_id: int) -> Path:
    """Gets the absolute path to the specified resource's data (i.e., parquet) file.

    Args:
        package_id: ID of the package.
        resource_id: ID of the resource.

    Returns:
        The absolute path the specified resource's data file.
    """
    path = path_resource(package_id, resource_id) / "data.parquet"
    return check_is_file(path)


def path_resource_raw(package_id: int, resource_id: int) -> Path:
    """Gets the absolute path to the specified resource's raw folder.

    Args:
        package_id: The ID of the package.
        resource_id: The ID of the resource.

    Returns:
        The absolute path to the specified resource's raw folder.
    """
    path = path_resource(package_id, resource_id) / "raw"
    return check_is_dir(path)


def path_resource_raw_files(package_id: int, resource_id: int) -> list[Path]:
    """Gets the absolute path to the raw files of the specified resource.

    Args:
        package_id: The ID of the package.
        resource_id: The ID of the resource.

    Returns:
        A list of paths to the specified resource's raw files.

    Raises:
        NotADirectoryError: If the package_id doesn't exist or the resource_id doesn't
            exist within the package.
    """
    return list(path_resource_raw(package_id, resource_id).iterdir())


def path_resources(package_id: int) -> Path:
    """Gets the absolute path to the resources of the specified package.

    Args:
        package_id: The ID of the package.

    Returns:
        The absolute path to the resources within the specified package.
    """
    path = path_package(package_id) / "resources"
    check_is_dir(path)
    return path
