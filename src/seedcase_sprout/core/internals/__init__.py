"""Internal functions for the package."""

from .check import _check_is_dir, _check_is_file
from .functionals import _map, _map2
from .read import _read_json

__all__ = [
    "_check_is_file",
    "_check_is_dir",
    "_map",
    "_map2",
    "_read_json",
]
