"""Internal functions for the package."""

from .check import _check_is_dir, _check_is_file
from .functionals import _map

__all__ = [
    "_check_is_file",
    "_check_is_dir",
    "_map",
]
