from os import getenv
from pathlib import Path


def get_root_envvar() -> Path | None:
    """Gets the root environment variable SPROUT ROOT if it exists.

    Returns:
        The path containing SPROUT_ROOT if it is set, otherwise None.
    """
    root = getenv("SPROUT_ROOT")
    return Path(root) if root else None
