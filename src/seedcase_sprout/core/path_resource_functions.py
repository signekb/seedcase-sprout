"""This module contains functions to get the paths to data resources and their files.

They are intended to be used in conjunction with other functions to read, write, and
edit the contents and properties of resources.
"""

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

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package and resource structure first
            sp.create_package_structure(path=sp.path_packages())
            sp.create_resource_structure(path=sp.path_resources(package_id=1))

            # Get the path to the resource
            sp.path_resource(package_id=1, resource_id=1)
        ```
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

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package and resource structure first
            sp.create_package_structure(path=sp.path_packages())
            sp.create_resource_structure(path=sp.path_resources(package_id=1))

            # TODO: Add data to resource
            # sp.write_resource_data_to_raw(
            #   package_id=1,
            #   resource_id=1,
            #   data="path/to/data.csv")

            # sp.write_resource_parquet(
            #     raw_files=sp.path_resource_raw_files(package_id=1, resource_id=1),
            #     path=sp.path_resource_data(package_id=1, resource_id=1))

            # Get the path to the resource data
            # sp.path_resource_data(package_id=1, resource_id=1)
        ```
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

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package and resource structure first
            sp.create_package_structure(path=sp.path_packages())
            sp.create_resource_structure(path=sp.path_resources(package_id=1))

            # Get the path to the resource's raw folder
            sp.path_resource_raw(package_id=1, resource_id=1)
        ```
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

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package and resource structure first
            sp.create_package_structure(path=sp.path_packages())
            sp.create_resource_structure(path=sp.path_resources(package_id=1))

            # TODO: Add data/raw files to resource
            # sp.write_resource_data_to_raw(
            #     path=sp.path_resource_raw(package_id=1, resource_id=1),
            #     data="path/to/data.csv")

            # Get the path to the resource's raw files
            sp.path_resource_raw_files(package_id=1, resource_id=1)
        ```
    """
    return list(path_resource_raw(package_id, resource_id).iterdir())


def path_resources(package_id: int) -> Path:
    """Gets the absolute path to the resources of the specified package.

    Args:
        package_id: The ID of the package.

    Returns:
        The absolute path to the resources within the specified package.

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package structure first
            sp.create_package_structure(path=sp.path_packages())

            # Get the path to the resource's raw files
            sp.path_resources(package_id=1)
        ```
    """
    path = path_package(package_id) / "resources"
    check_is_dir(path)
    return path
