"""This module contains functions to get the paths to data packages and their files.

They are intended to be used in conjunction with other functions to read, write, and
edit the contents and properties of packages.
"""

from pathlib import Path

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.check_is_file import check_is_file
from seedcase_sprout.core.check_is_package_dir import check_is_package_dir
from seedcase_sprout.core.create_dirs import create_dir
from seedcase_sprout.core.path_sprout_global import path_sprout_global


def path_package(package_id: int) -> Path:
    """Get the path to a specific package in Sprout's global location.

    If you want to get the location of the global packages directory,
    see `path_sprout_global()`.

    Args:
        package_id: The ID of the package.

    Returns:
        The absolute path to the specified package found in `SPROUT_GLOBAL`.

    Examples:
        ```{python}
        import os
        import tempfile
        from pathlib import Path

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Create a package structure first
            sp.create_package_structure(path=sp.path_packages())

            # Get the path to the package
            sp.path_package(package_id=1)
        ```
    """
    path = path_packages() / str(package_id)
    return check_is_package_dir(path)


def path_properties(package_id: int) -> Path:
    """Gets the absolute path to the specified package's properties file.

    Args:
        package_id: The ID of the package.

    Returns:
        The absolute path to the specified package's properties file.

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

            # Get the path to the package properties
            sp.path_properties(package_id=1)
        ```
    """
    path = path_package(package_id) / "datapackage.json"
    return check_is_file(path)


def path_packages() -> Path:
    """Get the paths for all packages in Sprout's global location.

    If you want to get the location of the global packages directory,
    see `path_sprout_global()`.

    Returns:
        The absolute path to the packages folder.

    Raises:
        NotADirectoryError: If the packages folder doesn't exist.

    Examples:
        ```{python}
        import os
        import tempfile

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Get the path to the packages folder
            sp.path_packages()
        ```
    """
    path = path_sprout_global() / "packages"
    return create_dir(path) if not path.exists() else check_is_dir(path)
