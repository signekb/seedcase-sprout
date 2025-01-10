from os import getenv
from pathlib import Path


def get_sprout_global_envvar() -> Path | None:
    """Gets the global environment variable `SPROUT_GLOBAL` if it exists.

    Returns:
        The path containing `SPROUT_GLOBAL` if it is set, otherwise None.
    """
    sprout_global = getenv("SPROUT_GLOBAL")
    return Path(sprout_global) if sprout_global else None
