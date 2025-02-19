from pathlib import Path

from seedcase_sprout.core.create_sprout_global_path import create_sprout_global_path
from seedcase_sprout.core.get_sprout_global_envvar import get_sprout_global_envvar


def path_sprout_global() -> Path:
    """Gets Sprout's global path location.

    If the `SPROUT_GLOBAL` environment variable isn't provided, this function
    will return the default path to where data packages will be stored. The
    default locations are dependent on the operating system.  This function also
    creates the necessary directory if it doesn't exist.

    Returns:
        The path to Sprout's global directory.

    Examples:
        ```{python}
        import tempfile
        import os

        import seedcase_sprout.core as sp

        # Create a temporary directory for the example
        with tempfile.TemporaryDirectory() as temp_dir:
            os.environ["SPROUT_GLOBAL"] = temp_dir

            # Get the path to Sprout's global directory
            sp.path_sprout_global()
        ```
    """
    return get_sprout_global_envvar() or create_sprout_global_path()
