import polars as pl

from seedcase_sprout.core.constants import BATCH_TIMESTAMP_COLUMN_NAME
from seedcase_sprout.core.properties import ResourceProperties
from seedcase_sprout.core.sprout_checks.check_data import check_data
from seedcase_sprout.core.sprout_checks.check_properties import (
    check_resource_properties,
)


def join_resource_batches(
    data_list: list[pl.DataFrame], resource_properties: ResourceProperties
) -> pl.DataFrame:
    """Joins all batch resource DataFrames into a single (Polars) DataFrame.

    This function takes a list of DataFrames, joins them together and drops any
    duplicate observational units based on the primary key from `resource_properties`.
    Then, it confirms that the data are correct against the `resource_properties` after
    the join.

    The observational unit is the primary key of the resource. For example, if a person
    is part of a research study and has multiple observations, the person's ID and the
    date of collection would be the observational unit.

    If there are any duplicate observational units in the data, only the most recent
    observational unit will be kept based on the timestamp of the batch file. This way,
    if there are any errors or mistakes in older batch files that have been corrected in
    later files, the mistake will be kept in the batch file, but won't be included in
    the `data.parquet` file.

    Args:
        data_list: A list of Polars DataFrames for all the batch files. Use
            `read_resource_batches()` to get a list of DataFrames that have been
            checked against the properties individually.
        resource_properties: The `ResourceProperties` object that contains the
            properties of the resource to check the data against.

    Returns:
        Outputs a single DataFrame object of all the batch data with duplicate
            observational units removed.

    Raises:
        polars.exceptions.ShapeError: Raised when dataframes in data_list have different
            shapes, such as mismatched column names or numbers.

        polars.exceptions.SchemaError: Raised when dataframes in data_list have
            different schemas, e.g., their column data types don't match.

    Examples:
        ```{python}
        import polars as pl

        import seedcase_sprout.core as sp
        # TODO: Remove this once read_properties/examples is done
        from seedcase_sprout.core.constants import BATCH_TIMESTAMP_COLUMN_NAME

        data_list = [
            pl.DataFrame(
                {
                    "id": [0, 1],
                    "name": ["anne", "belinda"],
                    "value": [0.0, 1.1],
                    # timestamp col from `read_resource_batches`
                    BATCH_TIMESTAMP_COLUMN_NAME: ["2025-03-26T100000Z"] * 2,
                }
            ),
            pl.DataFrame(
                {
                    "id": [2, 3, 0, 0, 0],
                    "name": ["catherine", "dorothy", "anne", "anne", "alberta"],
                    "value": [2.2, 3.3, 0.0, 9.9, 0.0],
                    # timestamp col from `read_resource_batches`
                    BATCH_TIMESTAMP_COLUMN_NAME: ["2024-03-26T100000Z"] * 5,
                }
            ),
        ]

        # Only the latest row with id = 0 is kept
        sp.join_resource_batches(
            data_list=data_list,
            resource_properties=sp.example_resource_properties(),
        )
        ```
    """
    check_resource_properties(resource_properties)

    data = pl.concat(data_list)
    primary_key = resource_properties.schema.primary_key
    data = _drop_duplicate_obs_units(data, primary_key)

    check_data(data, resource_properties)

    return data


def _drop_duplicate_obs_units(
    data: pl.DataFrame, primary_key: list[str] | str | None
) -> pl.DataFrame:
    """Drop duplicates based on the primary key and keep the latest one."""
    data = data.sort(BATCH_TIMESTAMP_COLUMN_NAME)
    data = data.drop(BATCH_TIMESTAMP_COLUMN_NAME)

    return data.unique(subset=primary_key, keep="last")
