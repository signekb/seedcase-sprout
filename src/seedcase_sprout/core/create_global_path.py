from pathlib import Path

from platformdirs import user_data_path


def create_global_path() -> Path:
    """Creates the path to Sprout global location.

    Returns:
        A Path with the Sprout global directory tied to the user.
    """
    return user_data_path("sprout")
