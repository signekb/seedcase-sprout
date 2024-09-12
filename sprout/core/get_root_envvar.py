from os import getenv
from pathlib import Path


def get_root_envvar() -> Path | None:
    """Get the root environment variable SPROUT ROOT if it exists.

    Returns:
        A Path object containing SPROUT_ROOT if it is set, otherwise None.
    """
    root = getenv("SPROUT_ROOT")
    return Path(root) if root else None
