from pathlib import Path

from seedcase_sprout.core.check_is_dir import check_is_dir
from seedcase_sprout.core.get_ids import get_ids


def check_is_package_dir(path: Path) -> Path:
    """Checks that the path is a directory within the package directory.

    Args:
        path: The path to verify.

    Returns:
        The path if it's a directory within the package directory.

    Raises:
        NotADirectoryError: If the path is not a directory. The error message
            includes existing IDs.
    """
    try:
        return check_is_dir(path)
    except NotADirectoryError as error:
        raise NotADirectoryError(
            f"This path can't be found, did you use the correct package ID?"
            f"- Existing IDs: {get_ids(path.parent)}"
        ) from error
