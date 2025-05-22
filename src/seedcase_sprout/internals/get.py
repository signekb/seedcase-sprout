from datetime import datetime


def _get_iso_timestamp() -> str:
    """Gets the current ISO timestamp compliant with the Data Package spec.

    Returns:
        The current ISO timestamp as a string. E.g. `2024-05-14T05:00:01+00:00`.
    """
    return datetime.now().astimezone().isoformat(timespec="seconds")
