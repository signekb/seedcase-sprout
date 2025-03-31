# ruff: noqa
def check_data(data: DataFrame, resource_properties: ResourceProperties) -> DataFrame:
    """Checks that the DataFrame matches the requirements in the resource properties.

    Runs a few checks to compare between the data and the properties on the items:

    | Data | Properties |
    |:------|:------------|
    | Column names | `field.name` |
    | Column types | `field.types` |
    | Column values' types | `field.types` |
    | Column values' constraints | `field.constraints` |

    Error messages output generally in the format of:

    > # {data item}:
    >
    > There is a mismatch found:
    >
    > - In the properties: {mismatch}
    > - In the data: {mismatch}

    Args:
        data: A Polars DataFrame.
        resource_properties: The specific `ResourceProperties` for the `data`.

    Returns:
        Output the `data` if checks all pass.

    Raises:
        ExceptionGroup: A list of messages that highlight where there are differences
            between the data and the properties.

    Examples:
        ```{python}
        import seedcase_sprout as sp

        check_data(
            data=sp.example_data(),
            resource_properties=sp.example_resource_properties()
        )
        ```
    """
    check_resource_properties(resource_properties)

    # TODO: These individual checks have their own pseudocode files.
    _check_column_names(data, resource_properties)
    _check_column_types(data, resource_properties)
    _check_column_values_constraints(data, resource_properties)

    return data
