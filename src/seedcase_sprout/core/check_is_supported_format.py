from pathlib import Path

SUPPORTED_FORMATS = [
    "csv",
    "tsv",
    "xlsx",
    "xls",
    "json",
    "jsonl",
    "ndjson",
    "parq",
    "parquet",
]


class UnsupportedFormatError(Exception):
    """Raised if file format is not supported by Sprout."""

    def __init__(self, format, *args, **kwargs):
        """Initialises UnsupportedFormatError.

        Args:
            format: The extension of the unsupported format
            *args: Non-keyword arguments
            **kwargs: Keyword arguments
        """
        message = (
            f"File format '{format}' is not supported. Sprout currently "
            f"supports the following formats: {', '.join(SUPPORTED_FORMATS)}."
        )
        super().__init__(message, *args, **kwargs)


def check_is_supported_format(path: Path) -> Path:
    """Checks that the format of the file given by the path is supported by Sprout.

    Args:
        path: The path pointing to the file to check

    Returns:
        The path pointing to the file, if the file format is supported

    Raises:
        UnsupportedFormatError: If the file format is not supported
    """
    format = path.suffix[1:]
    if format not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(format)
    return path
