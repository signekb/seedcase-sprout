"""Helper functions related to uploading files."""

import os
from typing import IO

from config.settings import PERSISTENT_STORAGE_PATH


def upload_raw_file(file: IO, output_file: str) -> str:
    """Upload and save a file into raw storage.

    Args:
        file: The file to persist
        output_file: The name of the file to store in raw storage.

    Returns:
        str: A character string of the path to the saved file.
    """
    raw_folder = f"{PERSISTENT_STORAGE_PATH}/raw"
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder)

    # Unique file path in the raw folder
    output_path = f"{raw_folder}/{output_file}"

    # Begin reading of file at the start of it
    file.seek(0)

    # Save to the location.
    with open(output_path, "wb") as target:
        target.write(file.read())

    return output_path
