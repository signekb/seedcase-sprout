from pathlib import Path

from seedcase_sprout.core.create_global_path import create_global_path
from seedcase_sprout.core.get_global_envvar import get_global_envvar


def path_sprout_global() -> Path:
    """Get Sprout's global path location.

    Returns:
        A Path to Sprout's global directory.
    """
    return get_global_envvar() or create_global_path()
