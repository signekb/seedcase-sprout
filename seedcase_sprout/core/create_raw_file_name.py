from pathlib import Path
from uuid import uuid4

from seedcase_sprout.core.get_iso_timestamp import get_compact_iso_timestamp


def create_raw_file_name(path: Path) -> str:
    """Creates a unique filename for a raw file.

    Args:
        path: The path to the raw file to extract the original extension from.

    Returns:
        The created raw file name in the format {timestamp}-{uuid}{ext}.gz
    """
    return f"{get_compact_iso_timestamp()}-{uuid4()}{path.suffix}.gz"
