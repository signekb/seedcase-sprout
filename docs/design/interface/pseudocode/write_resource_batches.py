# ruff: noqa
def write_resource_batch(
    data: pl.DataFrame, resource_properties: ResourceProperties
) -> Path:
    """Writes the tidied, original data (as a DataFrame) into the resource's batch data folder.

    Writes the original data that's been read in as a Polars DataFrame
    into the resource location available from the `path` property of the
    `resource_properties`. This will save a timestamped, unique file
    name to store it as a backup. See the
    [design](https://sprout.seedcase-project.org/docs/design/) docs for an
    explanation of this batch file. Data is always checked against the properties
    before saving into the batch folder. Copies and compresses the file, and
    outputs the path object of the created file.

        Args:
            data: A Polars DataFrame object with the data to write to the batch folder.
                Use `read_resource_batches()` and `join_resource_batches()` to get the
                data ready to write.
            resource_properties: The properties object for the specific resource.
                Use `read_properties()` to read the properties for the resource
                and `get_properties()` to get the correct resource properties.

        Returns:
            The path to the written Parquet resource file.

        Examples:
            ```{python}
            #| eval: false
            ```
    """
    check_data(data, resource_properties)
    # Since `path` is to the `data.parquet` file, take the `parent` to get the `batch` folder.
    batch_dir = Path(resource_properties.path.parent / "batch")

    batch_resource_path = Path(batch_dir / create_batch_file_name())
    return write_parquet(data, batch_resource_path)
