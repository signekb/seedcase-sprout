from pathlib import Path

from seedcase_sprout.core.create_resource_structure import create_resource_structure


def create_test_package_structure(global_path: Path, package_id: int) -> Path:
    """Creates a package file structure (with empty files) for path function tests.

    Args:
        global_path: Global path to create the package structure.
        package_id: ID of the package to create.

    Returns:
        Path of package.
    """
    # TODO: Use `create_package_properties()` function here when has been implemented.
    path_package = global_path / "packages" / str(package_id)
    path_package.mkdir(parents=True)
    (path_package / "datapackage.json").touch()
    (path_package / "README.md").touch()

    return path_package


def create_test_resource_structure(
    path_package: Path, raw_files: str | list[str]
) -> list[Path]:
    """Creates a resource file structure (with empty files) for path function tests.

    Args:
        path_package: Path to package.
        resource_id: ID of the resource to create.
        raw_files: Name(s) of raw file(s).

    Returns:
        List with two Paths: one to the resource, one to its raw directory.
    """
    path_resources = path_package / "resources"
    path_resources.mkdir(parents=True, exist_ok=True)

    path_list_resource = create_resource_structure(path_resources)
    (path_list_resource[0] / "data.parquet").touch()
    for raw_file in raw_files:
        (path_list_resource[1] / raw_file).touch()

    return path_list_resource
