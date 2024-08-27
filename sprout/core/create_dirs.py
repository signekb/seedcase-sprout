from pathlib import Path


def create_dir(path: Path) -> Path:
    """Creates a directory from a path.

    The path has already been verified as not existing.

    Args:
        path: The path pointing to the new directory to create

    Returns:
        path to the newly created directory.
    """
    path.mkdir(parents=True)
    return path


def create_dirs(paths: list[Path]) -> list[Path]:
    """Creates directories from a list of paths using the function create_dir.

    Args:
        paths: A list of paths pointing to where directories should be created.

    Returns:
        A list of paths to the newly created directories.
    """
    created_dirs = [create_dir(path) for path in paths]
    return created_dirs
