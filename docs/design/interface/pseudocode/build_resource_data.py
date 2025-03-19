# ruff: noqa
def build_resource_data(
    batch_files_path: list[Path], resource_properties: ResourceProperties
) -> DataFrame:
    """Merge all batch resource file(s) into a single (Polars) DataFrame.

    This function takes the file(s) given by `batch_files_path`, merges them
    together, does some checks and minor processing before outputting them as a
    single (Polars) DataFrame. The `resource_properties` object is used to check
    the data and ensure it is correct. This function doesn't write to Parquet,
    so that you can apply any additional processing to the data before saving it
    as a Parquet file.  While Sprout generally assumes that the files stored in
    the `resources/<id>/batch/` folder are already correctly structured and
    tidy, this function still runs checks to ensure the data are correct by
    comparing to the properties. All data in the `resources/<id>/batch/` folder
    will be merged into one single DataFrame object for either continued
    processing or to write to the Parquet file.

    If there are any duplicate observational units in the data, only the most recent
    observational unit will be kept. This way, if there are any errors or mistakes
    in older batch files that have been corrected in later files, the mistake can still
    be kept, but won't impact the data that will actually be used.

    Examples:

        ``` python
        import seedcase_sprout.core as sp

        sp.build_resource_data(
            batch_files_path=sp.path_resources_batch_files(1),
            resource_properties=sp.example_resource_properties,
        )
        ```

    Args:
        batch_files_path: A list of paths for all the batch files, mostly commonly
            stored in the `.csv.gz` format. Use `path_resource_batch_files()` to help
            provide the correct paths to the batch files.
        resource_properties: The `ResourceProperties` object that contains the properties
            of the resource you want to check the data against.

    Returns:
        Outputs a single DataFrame object of all the merged batch files.
    """
    # Not sure if this is the correct way to verify multiple files.
    [check_is_file(path) for path in batch_files_path]
    check_resource_properties(resource_properties)

    data = read_batch_files(batch_files_path)
    data = drop_duplicate_obs_units(data)

    # This function could be several functions or the one full function.
    check_data(data, resource_properties)

    return data


def read_batch_files(paths: list[Path]) -> DataFrame:
    # Can read gzip files.
    data_list = [polars.read_csv(path) for path in paths]
    # Merge them all together.
    data = polars.concat(data_list)
    return data


def drop_duplicate_obs_units(data: DataFrame) -> DataFrame:
    # Drop duplicates based on the observation unit, keeping only the most
    # recent one. This allows older batch files to contain potentially wrong
    # data that was corrected in the most recent file.
    return data.drop_duplicates()
