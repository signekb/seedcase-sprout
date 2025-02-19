def create_next_id(ids: list[int]) -> int:
    """Creates the next ID in a sequence, given a list of existing IDs. Starts at 1.

    Args:
        ids: The list of existing IDs.

    Returns:
        The newly generated ID.
    """
    return max(ids) + 1 if ids else 1
