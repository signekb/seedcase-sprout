from datetime import datetime
from pathlib import Path
from uuid import uuid4

import polars as pl

from seedcase_sprout.core.check_data import check_data
from seedcase_sprout.core.check_properties import (
    check_resource_properties,
)
from seedcase_sprout.core.constants import BATCH_TIMESTAMP_FORMAT
from seedcase_sprout.core.paths import PackagePath
from seedcase_sprout.core.properties import ResourceProperties


def write_resource_batch(
    data: pl.DataFrame,
    resource_properties: ResourceProperties,
    package_path: Path | None = None,
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
            is located). Defaults to the current working directory.

    Returns:
        The path to the written Parquet resource file.

    Raises:
        ExceptionGroup: A group of `CheckError`s, if resource properties are incorrect.
        # TODO: Add exception for data check when implemented.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp

        with sp.ExamplePackage():
            resource_properties = sp.read_properties().resources[0]
            sp.write_resource_batch(
                data=sp.example_data(),
                resource_properties=resource_properties,
            )
        ```
    """
    check_resource_properties(resource_properties)
    check_data(data, resource_properties)

    batch_path = PackagePath(package_path).resource_batch(resource_properties.name)
    batch_path.mkdir(exist_ok=True, parents=True)
    # TODO: Move out some of this into the create_batch_file_name during refactoring
    batch_file_path = batch_path / _create_batch_file_name()

    data.write_parquet(batch_file_path)

    return batch_file_path


def _create_batch_file_name() -> Path:
    return Path(f"{_get_compact_iso_timestamp()}-{uuid4()}.parquet")


def _get_compact_iso_timestamp() -> str:
    """Gets the current timestamp in a compact ISO format.

    Returns:
        The current compact ISO timestamp as a string in the format defined by
        BATCH_TIMESTAMP_FORMAT.
    """
    return datetime.now().strftime(BATCH_TIMESTAMP_FORMAT)
