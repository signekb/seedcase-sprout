from pytest import mark, raises

from seedcase_sprout.core.verify_is_supported_format import (
    SUPPORTED_FORMATS,
    UnsupportedFormatError,
    verify_is_supported_format,
)


@mark.parametrize("extension", SUPPORTED_FORMATS)
def test_accepts_supported_format(tmp_path, extension):
    """Given a supported file format, should return the path to the file."""
    file_path = tmp_path / f"test.{extension}"
    assert verify_is_supported_format(file_path) == file_path


@mark.parametrize("suffix", [".xyz", ".rtf", ".tar.gz", ".123", ".*^%#", ". ", ".", ""])
def test_rejects_unsupported_format(tmp_path, suffix):
    """Given an unsupported file format, should raise an UnsupportedFormatError."""
    file_path = tmp_path / f"test{suffix}"
    with raises(UnsupportedFormatError):
        verify_is_supported_format(file_path)
