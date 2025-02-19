from pathlib import Path

from frictionless import describe


def extract_properties_from_file(path: Path) -> dict:
    """Extracts the resource properties from the provided data file.

    Args:
        path: The path pointing to the data file.

    Returns:
        The dictionary of the resource properties.
    """
    return describe(path).to_dict()
