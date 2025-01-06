import json
from pathlib import Path

from seedcase_sprout.core.write_file import write_file


def write_json(json_object: list | dict, path: Path) -> Path:
    """Writes an object as an indented JSON string to the specified location.

    Args:
        json_object: The object to write to the file. Must be JSON serialisable.
        path: The path to the file with name and extension.

    Returns:
        The path to the newly created JSON file.

    Raises:
        FileNotFoundError: If the parent folder of the file doesn't exist.
        TypeError: If the object is not JSON serialisable.
    """
    return write_file(json.dumps(json_object, indent=2), path)
