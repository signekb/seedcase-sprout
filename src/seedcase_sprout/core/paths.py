"""This module contains functions to get the paths to various data package files.

They are intended to be used in conjunction with other functions to read, write, and
edit the contents and properties of various files within a data package. Specifically,
they are used in the context of a data package stored in the working directory ("local"
first approach).
"""

from pathlib import Path


class PackagePath:
    """Gets the absolute path to a specific file or folder in a data package.

    The functions in this class are used to get the absolute path to a specific file or
    folder in a data package. They are intended as convenience functions to provide
    easy and quick access to required files and folders within a data package.
    These functions have these characteristics in common:

    -   All of these functions output a `Path` object.
    -   The base class has an optional `path` argument that defaults to
        the current working directory available from the base class.
    -   If the wrong `resource_name` is given, an error message will include a
        list of all the actual `resource_name`'s for a specific package.

    Args:
        path: Provide a path to the package directory. Defaults to the current working
            directory.

    Returns:
        The absolute path to the data package's file or folder.

    Examples:
        ```{python}
        import tempfile
        import seedcase_sprout.core as sp

        sp.PackagePath().properties()
        sp.PackagePath().readme()

        # Create a temporary directory for the example to show
        # how to use the function with a different path
        with tempfile.TemporaryDirectory() as temp_path:
            sp.PackagePath(temp_path).properties()
            sp.PackagePath(temp_path).readme()
        ```
    """

    def __init__(self, path: Path = Path.cwd()) -> Path:
        """Set the base path."""
        self.path = path

    def properties(self) -> Path:
        """Path to the `datapackage.json` file."""
        return Path(self.path) / "datapackage.json"

    def readme(self) -> Path:
        """Path to the `README.md` file."""
        return Path(self.path) / "README.md"

    def resources(self) -> Path:
        """Path to the `resources/` folder."""
        return Path(self.path) / "resources"

    def resource(self, resource_name: str) -> Path:
        """Path to the specified `resources/<name>/` folder.

        Args:
            resource_name: The name of the resource. Use `ResourceProperties.name` to
                get the correct resource name.
        """
        return Path(self.path) / "resources" / str(resource_name)

    def resource_data(self, resource_name: str) -> Path:
        """Path to the specific resource's data file.

        Args:
            resource_name: The name of the resource. Use `ResourceProperties.name` to
                get the correct resource name.
        """
        return Path(self.path) / "resources" / str(resource_name) / "data.parquet"

    def resource_batch(self, resource_name: str) -> Path:
        """Path to the specific resource's `batch/` folder.

        Args:
            resource_name: The name of the resource. Use `ResourceProperties.name` to
                get the correct resource name.
        """
        return Path(self.path) / "resources" / str(resource_name) / "batch"

    def resource_batch_files(self, resource_name: str) -> Path:
        """Path to all the files in the specific resource's `batch/` folder.

        Args:
            resource_name: The name of the resource. Use `ResourceProperties.name` to
                get the correct resource name.
        """
        # TODO: This needs a check if the folder exists?
        return list(
            Path(Path(self.path) / "resources" / str(resource_name) / "batch").iterdir()
        )
