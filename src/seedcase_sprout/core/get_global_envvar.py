from os import getenv
from pathlib import Path


def get_global_envvar() -> Path | None:
    """Get the global environment variable `SPROUT_GLOBAL` if it exists.

    Returns:
        A Path object containing `SPROUT_GLOBAL` if it is set, otherwise None.
    """
    path = getenv("SPROUT_GLOBAL")
    return Path(path) if path else None
