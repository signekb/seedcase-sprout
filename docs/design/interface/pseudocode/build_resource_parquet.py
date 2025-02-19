# ruff: noqa
def build_resource_parquet(
    raw_files_path: list[Path], resource_properties: ResourceProperties
) -> Path:
    """Merge all raw resource file(s) and write into a Parquet file.

    This function takes the file(s) provided by `raw_files_path` and merges them into
    a `data.parquet` file. The Parquet file will be stored at the path found in `ResourceProperties.path`.
    While Sprout generally assumes
    that the files stored in the `resources/raw/` folder are already correctly
    structured and tidy, it still runs checks to ensure the data are correct
    by comparing to the properties. All data in the
    `resources/raw/` folder will be merged into one single data object and then
    written back to the Parquet file. The Parquet file will be overwritten.

    If there are any duplicate observation units in the data, only the most recent
    observation unit will be kept. This way, if there are any errors or mistakes
    in older raw files that have been corrected in later files, the mistake can still
    be kept, but won't impact the data that will actually be used.

    Examples:

        ``` python
        import seedcase_sprout.core as sp

        sp.build_resource_parquet(
            raw_files_path=sp.path_resources_raw_files(1),
            resource_properties=sp.example_resource_properties,
        )
        ```

    Args:
        raw_files_path: A list of paths for all the raw files, mostly commonly stored in the
            `.csv.gz` format. Use `path_resource_raw_files()` to help provide the
            correct paths to the raw files.
        resource_properties: The `ResourceProperties` object that contains the properties
            of the resource you want to create the Parquet file for.

    Returns:
        Outputs the path object of the created Parquet file.
    """
    # Not sure if this is the correct way to verify multiple files.
    [check_is_file(path) for path in raw_files_path]
    check_resource_properties(resource_properties)

    data = read_raw_files(raw_files_path)
    data = drop_duplicate_obs_units(data)

    # This function could be several functions or the one full function.
    check_data(data, resource_properties)

    return write_parquet(data, resource_properties["path"])


def write_parquet(data: DataFrame, path: Path) -> Path:
    return path


def read_raw_files(paths: list[Path]) -> DataFrame:
    # Can read gzip files.
    data_list = [polars.read_csv(path) for path in paths]
    # Merge them all together.
    data = polars.concat(data_list)
    return data


def drop_duplicate_obs_units(data: DataFrame) -> DataFrame:
    # Drop duplicates based on the observation unit, keeping only the most
    # recent one. This allows older raw files to contain potentially wrong
    # data that was corrected in the most recent file.
    return data.drop_duplicates()
