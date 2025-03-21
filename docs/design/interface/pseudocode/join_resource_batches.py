# ruff: noqa
def join_resource_batches(
    data_list: list[DataFrame], resource_properties: ResourceProperties
) -> DataFrame:
    """Joins all batch resource DataFrames into a single (Polars) DataFrame.

    This function takes the list of DataFrames, joins them together, does a
    check to confirm the data are ok against the `resource_properties` after
    joining them together, and then drops any duplicate observational units. In
    this case, the observational unit is the primary key or keys of all the
    resources in the data package. For example, if a person is part of a
    research study and has multiple observations, the person's ID and the date
    of collection would be the observational unit.

    If there are any duplicate observational units in the data, only the most
    recent observational unit will be kept based on the timestamp of the batch
    file. This way, if there are any errors or mistakes in older batch files
    that have been corrected in later files, the mistake will be kept in the batch file, but
    won't be included in the `data.parquet` file.
    ```

    Examples:

        ``` python
        import seedcase_sprout.core as sp

        sp.join_resource_batches(
            data_list=[DataFrame],
            resource_properties=sp.example_resource_properties(),
        )
        ```

    Args:
        data_list: A list of Polars DataFrames for all the batch files. Use
            `read_resource_batches()` to get a list of DataFrames that have been
            checked against the properties individually.
        resource_properties: The `ResourceProperties` object that contains the properties
            of the resource to check the data against.

    Returns:
        Outputs a single DataFrame object of all the batch data with duplicate
            observational units removed.
    """
    check_resource_properties(resource_properties)

    # Or join, but depends on how things are implemented here.
    data = polars.concat(data_list)
    data = drop_duplicate_obs_units(data, resource_properties)
    check_data(data, resource_properties)

    return data


# Not sure if the arg should be the properties or the keys themselves.
def drop_duplicate_obs_units(
    data: DataFrame, resource_properties: ResourceProperties
) -> DataFrame:
    # Drop duplicates based on the observation unit, keeping only the most
    # recent one. This allows older batch files to contain potentially wrong
    # data that was corrected in the most recent file.

    # Not sure how exactly this might be implemented. This is all pseudocode
    # right now.
    primary_keys = get_primary_keys(resource_properties)
    data = sort_by_timestamp(data)
    data = drop_duplicates(data, primary_keys)
    return data
