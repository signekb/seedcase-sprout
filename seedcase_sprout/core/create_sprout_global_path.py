from pathlib import Path

from platformdirs import user_data_path


def create_sprout_globalpath() -> Path:
    """Creates the path to Sprout global location.

    Returns:
        The path with the Sprout global directory tied to the user.
    """
    return user_data_path("sprout")
