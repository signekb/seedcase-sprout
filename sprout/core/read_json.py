from json import loads
from pathlib import Path


def read_json(path: Path) -> list | dict:
    """Loads the contents of a JSON file into an object.

    Args:
        path: The path to the file to load.

    Returns:
        The contents of the file as an object.

    Raises:
        JSONDecodeError: If the contents of the file cannot be deserialised as JSON.
    """
    return loads(path.read_text())
