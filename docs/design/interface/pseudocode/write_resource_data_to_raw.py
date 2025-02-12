# ruff: noqa
def write_resource_data_to_raw(data_path, resource_properties) -> Path:
    """Writes the raw data file into the resource's raw data folder.

    Copy the file from `data_path` over into the resource location given by
    `path`. This will compress the file and use a timestamped, unique file
    name to store it as a backup. See the
    [design](https://sprout.seedcase-project.org/docs/design/) docs for an
    explanation of this file. Data is always checked against the properties
    before saving into the raw folder. Copies and compresses the file, and
    outputs the path object of the created file.

        Args:
            data_path: Path to a raw data file that you want Sprout to store
                into the data package.
            resource_properties: The properties object for the specific resource.
                Use `read_properties()` to read the properties for the resource
                and `get_properties()` to get the correct resource properties.

        Returns:
            The path to the written compressed raw resource file.

        Examples:
            ```{python}
            #| eval: false
            ```
    """
    check_is_file(data_path)
    check_is_supported_format(data_path)
    check_data_basics(data_path, resource_properties)
    check_data_constraints(data_path, resource_properties)
    # Since `path` is to the `data.parquet` file.
    raw_dir = Path(resource_properties.path.parent / "raw")

    raw_resource_path = Path(raw_dir / create_raw_file_name(data_path))
    return write_compressed_file(data_path, raw_resource_path)


def create_raw_file_name(data_path: Path) -> str:
    """Creates a timestamped, unique file name for the raw data file.

    This function creates a timestamped, unique file name for the raw data file
    that is being copied into the resource's raw data folder. This file name
    is used to store the raw data file as a backup. The file name will be
    in the format `{timestamp}-{uuid}.{extension}.gz`, where `timestamp` is the
    current time following ISO8601 format, and `uuid` is a universally unique ID.

        Args:
            data_path: The path to the raw data file.

        Returns:
            A path to a (potentially) new raw resource file.
    """
    # Untested code.
    timestamp = datetime.datetime.now().isoformat()
    uuid = str(uuid.uuid4())
    extension = data_path.suffix
    return f"{timestamp}-{uuid}.{extension}.gz"


def write_compressed_file(data_path: Path, path: Path) -> Path:
    """Compress and write the raw data file into the resource's raw data folder.

    This function copies the raw data file from `data_path` to the resource's
    raw data folder, compressing it in the process. The compressed file is
    stored in the raw data folder based on the path provided.

        Args:
            data_path: The path to the raw data file.
            path: The path to the raw resource file in the
                resource's raw data folder.

        Returns:
            The path to the written compressed raw resource file.
    """
    return path


def check_data_basics(data_path: Path, resource_properties: ResourceProperties) -> Path:
    """Basic checks on the data against the resource properties.

    Checks the data for basic things, including against the specific resource's
    properties for things like:

    - Can it be at a minimal read without problems or warnings?
    - Do the columns in the data file match those in the properties?
    - Do the data types in the data file match those in the properties?

        Args:
            data_path: The path to the raw data file.
            resource_properties: The properties object for the specific resource.

        Returns:
            An error if the requirements are not met.
    """
    return None


def check_data_constraints(
    data_path: Path, resource_properties: ResourceProperties
) -> Path:
    """Check the data against the resource's constraints properties.

    The resource properties sometimes contains a `constraints` property
    for each column. This checks whether the data matches the constraints
    given in the properties.

        Args:
            data_path: The path to the raw data file.
            resource_properties: The properties object for the specific resource.

        Returns:
            An error if the constraints are not met, otherwise `None`.
    """
    # Check the data against the resource constraints properties.

    return None
