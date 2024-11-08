from pathlib import Path

SUPPORTED_FORMATS = [
    "csv",
    "tsv",
    "xlsx",
    "xls",
    "json",
    "jsonl",
    "ndjson",
    "geojson",
    "topojson",
    "ods",
    "parq",
    "parquet",
]


class UnsupportedFormatError(Exception):
    """Raised if file format is not supported by Sprout."""

    def __init__(self, format, *args, **kwargs):
        """Initialises UnsupportedFormatError.

        Args:
            format: the extension of the unsupported format
            *args: non-keyword arguments
            **kwargs: keyword arguments
        """
        message = (
            f"File format '{format}' is not supported. Sprout currently "
            f"supports the following formats: {', '.join(SUPPORTED_FORMATS)}."
        )
        super().__init__(message, *args, **kwargs)


def verify_is_supported_format(path: Path) -> Path:
    """Checks that the format of the file given by the path is supported by Sprout.

    Args:
        path: the path pointing to the file to check

    Raises:
        UnsupportedFormatError: raised if the file format is not supported

    Returns:
        the path pointing to the file, if the file format is supported
    """
    format = path.suffix[1:]
    if format not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(format)
    return path
