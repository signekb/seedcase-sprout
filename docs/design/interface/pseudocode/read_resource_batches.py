# ruff: noqa
def read_resource_batches(
    paths: list[Path], resource_properties: ResourceProperties
) -> list[DataFrame]:
    """Reads all the batch resource file(s) into a list of (Polars) DataFrames.

    This function takes the file(s) given by `paths`, reads them in as Polars
    DataFrames as a list and does some checks on each of the DataFrames in the list
    based on the `resource_properties`. The `resource_properties` object is used
    to check the data and ensure it is correct. While Sprout generally assumes
    that the files stored in the `resources/<id>/batch/` folder are already
    correctly structured and tidy, this function still runs checks to ensure the
    data are correct by comparing to the properties.

    Examples:

        ``` python
        import seedcase_sprout.core as sp

        sp.read_resource_batches(
            paths=sp.PackagePath().resources_batch_files(1),
            resource_properties=sp.example_resource_properties(),
        )
        ```

    Args:
        paths: A list of paths for all the files in the resource's `batch/` folder.
            Use `PackagePath().resource_batch_files()` to help provide the correct paths to the
            batch files.
        resource_properties: The `ResourceProperties` object that contains the properties
            of the resource you want to check the data against.

    Returns:
        Outputs a list of DataFrame objects from all the batch files.
    """
    # Not sure if this is the correct way to verify multiple files.
    map(check_is_file, paths)
    check_resource_properties(resource_properties)

    data_list = list(map(_read_parquet_batch, paths))

    list(map(check_data, data_list, resource_properties))

    return data_list


def _read_parquet_batch(path: Path) -> DataFrame:
    """Reads a single batch Parquet file into a Polars DataFrame and adds the timestamp as a column."""
    data = pl.read_parquet(path)
    timestamp = get_timestamp_from_path(path)
    check_timestamp(timestamp)
    # Take the timestamp from the file name and add it as a column to the data.
    # Not sure how this will be implemented exactly.
    data = add_timestamp_as_column(data, timestamp)
    return data
