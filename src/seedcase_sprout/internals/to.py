def _to_camel_case(text: str) -> str:
    """Converts snake case to camel case.

    Args:
        text: The snake-case string to convert.

    Returns:
        The converted string in camel case.
    """
    first_part, *remaining_parts = text.split("_")
    return first_part + "".join(part.title() for part in remaining_parts)
