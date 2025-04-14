from pathlib import Path

import polars as pl

from seedcase_sprout.core.create_batch_file_name import create_batch_file_name

# from seedcase_sprout.core.checks.check_data import check_data
from seedcase_sprout.core.paths import PackagePath
from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.sprout_checks.check_data import check_data
from seedcase_sprout.core.sprout_checks.check_properties import (
    check_resource_properties,
)


def write_resource_batch(
    data: pl.DataFrame,
    resource_properties: ResourceProperties,
    package_path: Path = Path.cwd(),
) -> Path:
    """Writes the tidied, original data into the resource's batch data folder.

    Writes the original data that is in a Tidy format and read as a pl.DataFrame
    into the resource location available from the `path` property of the
    `resource_properties`. This will save a timestamped, unique file
    name to store it as a backup. See the
    [design](https://sprout.seedcase-project.org/docs/design/) docs for an
    explanation of this batch file. Data is always checked against the properties
    before writing it to the batch folder.

    Args:
        data: A Polars DataFrame object with the data to write to the batch folder.
        resource_properties: The properties object for the specific resource.
            Use `read_properties()` to read the properties for the resource
            and `get_resource_properties()` to get the correct resource properties.
        package_path: The path to the data package root folder (where `datapackage.json`
            is located).

    Returns:
        The path to the written Parquet resource file.

    Raises:
        ExceptionGroup: A group of `CheckError`s, if resource properties are incorrect.
        # TODO: Add exception for data check when implemented.

    Examples:
        ```{python}
        import tempfile
        from pathlib import Path

        import polars as pl

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_path:
            # TODO: Update to use Sprout functions instead of creating folders manually
            (Path(temp_path) / "resources/example-resource").mkdir(parents=True)

            tidy_data = pl.DataFrame(
                {
                    "id": [0, 1, 2],
                    "name": ["anne", "belinda", "catherine"],
                    "value": [1.1, 2.2, 3.3],
                }
            )
            resource_properties = sp.example_resource_properties()

            sp.write_resource_batch(
                data=tidy_data,
                resource_properties=resource_properties,
                package_path=temp_path,
            )
        ```
    """
    check_resource_properties(resource_properties)
    check_data(data, resource_properties)

    batch_path = PackagePath(package_path).resource_batch(resource_properties.name)
    batch_path.mkdir(exist_ok=True)
    # TODO: Move out some of this into the create_batch_file_name during refactoring
    batch_file_path = batch_path / Path(create_batch_file_name()).with_suffix(
        ".parquet"
    )

    data.write_parquet(batch_file_path)

    return batch_file_path
