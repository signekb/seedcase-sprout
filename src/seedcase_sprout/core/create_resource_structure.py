from pathlib import Path

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.create_dirs import create_dirs
from seedcase_sprout.core.create_id_path import create_id_path
from seedcase_sprout.core.create_next_id import create_next_id
from seedcase_sprout.core.create_resource_raw_path import create_resource_raw_path
from seedcase_sprout.core.get_ids import get_ids


def create_resource_structure(path: Path) -> list[Path]:
    """Creates the directory structure of a new resource.

    This is the first function to use to set up the structure for a data
    resource. It creates the paths for a new data resource in a specific
    (existing) package by creating the folder setup described in the
    [Outputs](https://sprout.seedcase-project.org/docs/design/outputs) section
    on the Sprout website. It creates two paths: the `resources/<id>/` path and the
    `resources/<id>/raw/` path. The output is a list of these two path objects.

    Args:
       path: Path to the resources directory in a package.

    Returns:
       A list of the two created directories:
          - A path to the resource directory and
          - A path to the raw data directory.

    Raises:
       NotADirectoryError: If path is not an existing directory.

    Examples:
      ```{python}
      import tempfile
      from pathlib import Path

      import seedcase_sprout.core as sp

      # Create a temporary directory for the example
      with tempfile.TemporaryDirectory() as temp_dir:
         temp_path = Path(temp_dir)

         # Create a package structure first
         sp.create_package_properties(
            properties=sp.example_package_properties(),
            path=temp_path
        )

         # TODO: Update after converting to "local-first"
         # Create a resource structure
         # sp.create_resource_structure(path=temp_path / "1" / "resources")
      ```
    """
    check_is_dir(path)

    existing_ids = get_ids(path)
    next_id = create_next_id(existing_ids)

    resource_path = create_id_path(path, next_id)
    resource_raw_path = create_resource_raw_path(resource_path)

    return create_dirs([resource_path, resource_raw_path])
