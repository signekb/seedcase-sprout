from datetime import datetime

from seedcase_sprout.core.constants import BATCH_TIMESTAMP_FORMAT


def get_iso_timestamp() -> str:
    """Gets the current ISO timestamp compliant with the Data Package spec.

    Returns:
        The current ISO timestamp as a string. E.g. `2024-05-14T05:00:01+00:00`.
    """
    return datetime.now().astimezone().isoformat(timespec="seconds")


def get_compact_iso_timestamp() -> str:
    """Gets the current timestamp in a compact ISO format.

    Returns:
        The current compact ISO timestamp as a string in the format defined by
        BATCH_TIMESTAMP_FORMAT.
    """
    return datetime.now().strftime(BATCH_TIMESTAMP_FORMAT)
