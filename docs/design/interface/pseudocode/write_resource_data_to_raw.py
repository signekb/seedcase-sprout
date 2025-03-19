# ruff: noqa
def write_resource_batch_data(data_path, resource_properties) -> Path:
    """Writes the original data file into the resource's batch data folder.

    Copy the file from `data_path` over into the resource location given by
    `path`. This will compress the file and use a timestamped, unique file
    name to store it as a backup. See the
    [design](https://sprout.seedcase-project.org/docs/design/) docs for an
    explanation of this file. Data is always checked against the properties
    before saving into the batch folder. Copies and compresses the file, and
    outputs the path object of the created file.

        Args:
            data_path: Path to a raw data file that you want Sprout to store
                into the data package.
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
    check_is_file(data_path)
    check_is_supported_format(data_path)
    data = read_data(data_path)
    check_data(data, resource_properties)
    # Since `path` is to the `data.parquet` file.
    batch_dir = Path(resource_properties.path.parent / "batch")

    batch_resource_path = Path(batch_dir / create_batch_file_name(data_path))
    return write_parquet(data_path, batch_resource_path)


def create_batch_file_name(data_path: Path) -> str:
    """Creates a timestamped, unique file name for the batch data file.

    This function creates a timestamped, unique file name for the batch data file
    that is being copied into the resource's batch data folder. This file name
    is used to store the data file as a backup. The file name will be
    in the format `{timestamp}-{uuid}.{extension}.gz`, where `timestamp` is the
    current time following ISO8601 format, and `uuid` is a universally unique ID.

        Args:
            data_path: The path to the batch data file.

        Returns:
            A path to a (potentially) new batch resource file.
    """
    # Untested code.
    timestamp = datetime.datetime.now().isoformat()
    uuid = str(uuid.uuid4())
    extension = data_path.suffix
    return f"{timestamp}-{uuid}.{extension}.gz"
