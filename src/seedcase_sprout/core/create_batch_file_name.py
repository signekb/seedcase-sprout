from uuid import uuid4

from seedcase_sprout.core.get_iso_timestamp import get_compact_iso_timestamp


def create_batch_file_name() -> str:
    """Creates a unique filename for a batch file.

    Args:
        path: The path to the batch file to extract the original extension from.

    Returns:
        The created batch file name in the format {timestamp}-{uuid}
    """
    return f"{get_compact_iso_timestamp()}-{uuid4()}"
