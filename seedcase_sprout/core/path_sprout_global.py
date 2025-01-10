from pathlib import Path

from seedcase_sprout.core.create_sprout_global_path import create_sprout_globalpath
from seedcase_sprout.core.get_sprout_global_envvar import get_sprout_global_envvar


def path_sprout_global() -> Path:
    """Gets Sprout's global path location.

    Returns:
        The path to Sprout's global directory.
    """
    return get_sprout_global_envvar() or create_sprout_globalpath()
