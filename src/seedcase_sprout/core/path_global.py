"""This module contains functions to get the paths to data packages and their files.

They are intended to be used in conjunction with other functions to read, write, and
edit the contents and properties of packages. These functions in particular are used
for the global location of packages, in environments with potentially multiple users
and many data packages.
"""

from os import getenv
from pathlib import Path

from platformdirs import user_data_path

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.check_is_package_dir import check_is_package_dir
from seedcase_sprout.core.create_dirs import create_dir


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

            package_path = sp.path_packages() / "1"
            package_path.mkdir()
            # Create a package structure first
            sp.create_package_properties(
                properties=sp.example_package_properties(),
                path=package_path
            )

            # Get the path to the package
            sp.path_package(package_id=1)
        ```
    """
    path = path_packages() / str(package_id)
    return check_is_package_dir(path)


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


def path_sprout_global() -> Path:
    """Gets Sprout's global path location.

    If the `SPROUT_GLOBAL` environment variable isn't provided, this function
    will return the default path to where data packages will be stored. The
    default locations are dependent on the operating system.  This function also
    creates the necessary directory if it doesn't exist.

    Returns:
        The path to Sprout's global directory.

    Examples:
        ```{python}
        import tempfile
        import os

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Get the path to Sprout's global directory
            sp.path_sprout_global()
        ```
    """
    return _get_sprout_global_envvar() or _create_sprout_global_path()


def _create_sprout_global_path() -> Path:
    """Creates the path to Sprout global location.

    Returns:
        The path with the Sprout global directory tied to the user.
    """
    return user_data_path("sprout")


def _get_sprout_global_envvar() -> Path | None:
    """Gets the global environment variable `SPROUT_GLOBAL` if it exists.

    Returns:
        The path containing `SPROUT_GLOBAL` if it is set, otherwise None.
    """
    sprout_global = getenv("SPROUT_GLOBAL")
    return Path(sprout_global) if sprout_global else None
