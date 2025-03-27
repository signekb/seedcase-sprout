"""This module contains functions to get the paths to various data package files.

They are intended to be used in conjunction with other functions to read, write, and
edit the contents and properties of various files within a data package. Specifically,
they are used in the context of a data package stored in the working directory ("local"
first approach).
"""

from pathlib import Path

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.check_is_resource_dir import check_is_resource_dir


def path_properties(path: Path = Path.cwd()) -> Path:
    """Gets the absolute path to the specified package's properties file.

    Args:
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to the data package's properties file.

    Examples:
        ```{python}
        import os
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Create a package structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            sp.path_properties(path=temp_path)
        ```
    """
    path = path / "datapackage.json"
    return check_is_file(path)


def path_readme(path: Path = Path.cwd) -> Path:
    """Get the path to the README file for the data package.

    Args:
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to the data package's README file.

    Examples:
        ```{python}
        import os
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            sp.path_readme(path=temp_path)
        ```
    """
    path = path / "README.md"
    return check_is_file(path)


def path_resource(resource_id: int, path: Path = Path.cwd()) -> Path:
    """Gets the absolute path to the specified resource.

    Args:
        resource_id: The ID of the resource.
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to a specific resource in the data package.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package and resource structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            resources_path = Path(temp_path / "resources")
            resources_path.mkdir()
            sp.create_resource_structure(path=resources_path)

            # Get the path to the resource
            sp.path_resource(resource_id=1, path=temp_path)
        ```
    """
    path = path_resources(path=path) / str(resource_id)
    return check_is_resource_dir(path)


def path_resource_data(resource_id: int, path: Path = Path.cwd()) -> Path:
    """Gets the absolute path to a specific resource's data (i.e., Parquet) file.

    Args:
        resource_id: ID of the resource.
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path the specific resource's data file in a data package.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package and resource structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            # TODO: Update after writing data to resource
            # resource_path = Path(temp_path / "resources")
            # resource_path.mkdir()
            # sp.create_resource_structure(path=resource_path)
            # sp.write_resource_data_to_batch(
            #   package_id=1,
            #   resource_id=1,
            #   data="path/to/data.csv")

            # sp.write_resource_parquet(
            #         batch_files=sp.path_resource_batch_files(
            #             resource_id=1, path=temp_path
            #         ),
            #         path=sp.path_resource_data(resource_id=1, path=temp_path),
            #     )

            # Get the path to the resource data
            # sp.path_resource_data(resource_id=1, path=temp_path)
        ```
    """
    path = path_resource(resource_id, path=path) / "data.parquet"
    return check_is_file(path)


def path_resource_batch(resource_id: int, path: Path = Path.cwd()) -> Path:
    """Gets the absolute path to a specific resource's batch folder.

    Args:
        resource_id: The ID of the resource.
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to a specific resource's batch folder in a data package.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package and resource structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            resources_path = Path(temp_path / "resources")
            resources_path.mkdir()
            sp.create_resource_structure(path=resources_path)

            # Get the path to the resource's batch folder
            sp.path_resource_batch(resource_id=1, path=temp_path)
        ```
    """
    path = path_resource(resource_id, path=path) / "batch"
    return check_is_dir(path)


def path_resource_batch_files(resource_id: int, path: Path = Path.cwd()) -> list[Path]:
    """Gets the absolute path to the batch files of a specific resource.

    Args:
        resource_id: The ID of the resource.
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        A list of paths to a specific resource's batch files in a data package.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package and resource structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            resources_path = Path(temp_path / "resources")
            resources_path.mkdir()
            sp.create_resource_structure(path=resources_path)
            # TODO: Add data/batch files to resource
            # sp.write_resource_batch_data(
            #     path=sp.path_resource_batch(resource_id=1, path=temp_dir),
            #     data="path/to/data.csv")

            # Get the path to the resource's batch files
            # sp.path_resource_batch_files(resource_id=1, path=temp_dir)
        ```
    """
    return list(path_resource_batch(resource_id, path=path).iterdir())


def path_resources(path: Path = Path.cwd()) -> Path:
    """Gets the absolute path to the resources of a data package.

    Args:
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to the resource in a data package.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a package structure first
            sp.write_package_properties(
                properties=sp.example_package_properties(),
                path=Path(temp_path / "datapackage.json")
            )

            Path(temp_path / "resources").mkdir()
            # Get the path to the resource folders
            sp.path_resources(path=temp_path)
        ```
    """
    path = path / "resources"
    return check_is_dir(path)
