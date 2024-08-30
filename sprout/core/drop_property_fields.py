def drop_property_fields(properties: dict, fields: list[str]) -> dict:
    """Deletes the specified fields from the properties object.

    Ignores fields not in properties.

    Args:
        properties: the properties object to update
        fields: the name of the fields to delete

    Returns:
        the updated properties object
    """
    for field in fields:
        if field in properties:
            del properties[field]
    return properties
