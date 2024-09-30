from datetime import datetime


def get_iso_timestamp() -> str:
    """Generates a timestamp compliant with the Data Package spec.

    Returns:
        The timestamp as a string. E.g. `2024-05-14T05:00:01+00:00`.
    """
    return datetime.now().astimezone().isoformat(timespec="seconds")
