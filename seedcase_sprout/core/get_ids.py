import re
from pathlib import Path


def get_ids(path: Path) -> list[int]:
    """Gets the ids of existing resources or packages in a directory.

    Args:
        path: The directory to search for IDs.

    Returns:
        A list of integers representing the ids of the subdirectories.
            If no IDs are found, an empty list is returned.
    """
    # Keep only directories
    dirs = list(path.glob("*/"))
    ids = list(map(get_number_from_dir, dirs))
    # Drop any empty items
    ids = sorted(filter(None, ids))

    return ids


def get_number_from_dir(path: Path) -> int | None:
    """Gets only the number from the directory.

    Args:
        path: The directory to extract the number from.

    Returns:
        A single integer if the directory contains a number. Otherwise, None.
    """
    dir_name = path.name
    if re.match(r"^\d+$", dir_name):
        return int(dir_name)
