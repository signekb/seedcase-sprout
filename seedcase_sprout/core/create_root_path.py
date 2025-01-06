from pathlib import Path

from platformdirs import user_data_path


def create_root_path() -> Path:
    """Creates the path to Sprout root.

    Returns:
        The path with the Sprout root directory tied to the user.
    """
    return user_data_path("sprout")
