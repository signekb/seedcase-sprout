from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.core.create_resource_properties import create_resource_properties
from seedcase_sprout.core.not_properties_error import NotPropertiesError
from seedcase_sprout.core.properties import ResourceProperties


@fixture
def resource_properties():
    return ResourceProperties(
        name="resource-name",
        path="",
    )


def test_creates_properties_correctly(tmp_path, resource_properties):
    """Given valid inputs, should create properties object correctly."""
    resource_path = tmp_path / "resources" / "1"
    resource_path.mkdir(parents=True)

    expected_properties = ResourceProperties(
        name="resource-name", path=str(Path("resources", "1", "data.parquet"))
    )

    assert (
        create_resource_properties(resource_path, resource_properties)
        == expected_properties
    )


def test_rejects_path_if_invalid(tmp_path, resource_properties):
    """Given an invalid path input, should raise NotADirectoryError."""
    resource_path = tmp_path / "nonexistent"

    with raises(NotADirectoryError):
        create_resource_properties(resource_path, resource_properties)


def test_rejects_properties_if_incorrect(tmp_path):
    """Given an incorrect/empty properties input, should raise NotPropertiesError."""
    with raises(NotPropertiesError):
        create_resource_properties(tmp_path, ResourceProperties())
