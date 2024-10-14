from pathlib import Path

from sprout.core.create_default_package_properties import (
    create_default_package_properties,
)
from sprout.core.create_dirs import create_dir
from sprout.core.create_id_path import create_id_path
from sprout.core.create_next_id import create_next_id
from sprout.core.create_properties_path import create_properties_path
from sprout.core.create_readme_path import create_readme_path
from sprout.core.create_readme_text import create_readme_text
from sprout.core.get_ids import get_ids
from sprout.core.verify_is_dir import verify_is_dir
from sprout.core.write_file import write_file
from sprout.core.write_json import write_json


def create_package_structure(path: Path) -> list[Path]:
    """Sets up the folder structure for a new package.

    This is the first function to use to create a new data package. It assigns a package
    ID and then creates a package folder and all the necessary files for a package
    (excluding the resources), outputting the file paths for the created files.

    Args:
        path: The path to the folder containing the packages. Use `path_packages()`
            to provide the correct path location.

    Returns:
        A list of paths to the two created files: The datapackage.json and the
            README.md.

    Raises:
        NotADirectoryError: If the directory in the path doesn't exist.
        FileNotFoundError: If a file could not be created.
        TypeError: If `datapackage.json` could not be created.
    """
    verify_is_dir(path)
    ids = get_ids(path)
    id = create_next_id(ids)
    package_path = create_id_path(path, id)
    create_dir(package_path)

    properties = create_default_package_properties()
    properties_path = create_properties_path(package_path)
    readme = create_readme_text(properties)
    readme_path = create_readme_path(package_path)

    return [write_json(properties, properties_path), write_file(readme, readme_path)]
