def edit_property_field(properties: dict, field: str, value: any) -> dict:
    """Edits properties by setting the specified field to the specified value.

    Args:
        properties: The properties to edit.
        field: The name of the field to edit.
        value: The value to assign to the field.

    Returns:
        The updated properties object.

    Raises:
        KeyError: If the specified field does not exist in the properties.
    """
    if field not in properties:
        raise KeyError(f"Field '{field}' does not exist in properties {properties}.")

    properties[field] = value
    return properties
