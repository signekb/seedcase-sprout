# ruff: noqa
def _check_column_names(
    data: DataFrame, resource_properties: ResourceProperties
) -> str:
    """Check that column names in `data` match those in `resource_properties`.

    Args:
        data: The data to check.
        resource_properties: The resource properties to check against.

    Returns:
        The data if the column names match.

    Raises:
        TODO: Update this to the relevant check error.
        SomeCheckError: If the column names do not match then the error message will
            include which names are mismatching between the `data` and `resource_properties`.
    """
    check_resource_properties(resource_properties)

    names_in_data = data.schema.names()
    names_in_resource = _get_property_field_names(resource_properties)

    extra_columns_in_data = set(names_in_data) - set(names_in_resource)
    missing_columns_in_data = set(names_in_resource) - set(names_in_data)

    if extra_columns_in_data or missing_columns_in_data:
        # The error message could look something like the below:
        # "Columns in data that are missing or extra when compared to properties: "
        #
        # "- Extras: {extra_columns_in_data}."
        # "- Missing: {missing_columns_in_data}."
        #
        # Or if mismatch in e.g. data only:
        # "Columns in data that are not in the properties: "
        #
        # "- Columns: {difference_in_names}."
        # TODO: This function name is a placeholder for getting the message to look like above.
        error_message = _format_column_name_error_message(
            extra_columns_in_data, missing_columns_in_data
        )
        raise SomeCheckError(error_message)

    return data
