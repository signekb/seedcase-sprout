from pathlib import Path

from pytest import raises

from sprout.core.create_resource_properties import create_resource_properties
from sprout.core.not_properties_error import NotPropertiesError


def test_creates_properties_correctly(tmp_path):
    """Given valid inputs, should create properties object correctly."""
    resource_path = tmp_path / "resources" / "1"
    resource_path.mkdir(parents=True)
    properties = {
        "name": "test",
        "path": "",
    }
    expected_properties = {
        "name": "test",
        "path": str(Path("resources", "1", "data.parquet")),
    }

    assert create_resource_properties(resource_path, properties) == expected_properties


def test_rejects_path_if_invalid(tmp_path):
    """Given an invalid path input, should raise NotADirectoryError."""
    resource_path = tmp_path / "nonexistent"
    properties = {
        "name": "test",
        "path": "",
    }

    with raises(NotADirectoryError):
        create_resource_properties(resource_path, properties)


def test_rejects_properties_if_incorrect(tmp_path):
    """Given an incorrect properties input, should raise NotPropertiesError."""
    with raises(NotPropertiesError):
        create_resource_properties(tmp_path, {})
