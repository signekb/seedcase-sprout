from pathlib import Path

from frictionless import describe


def extract_properties_from_file(path: Path) -> dict:
    """Extracts resource properties from the provided data file.

    Args:
        path: the path pointing to the data file

    Returns:
        a dictionary of resource properties
    """
    return describe(path).to_dict()
