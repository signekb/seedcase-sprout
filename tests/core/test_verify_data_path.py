from pathlib import Path

from pytest import fixture, mark, raises

from sprout.core.not_properties_error import NotPropertiesError
from sprout.core.properties import ResourceProperties
from sprout.core.verify_data_path import verify_data_path


@fixture
def resource_properties() -> dict:
    return ResourceProperties(
        name="my-resource",
        path=str(Path("resources", "1", "data.parquet")),
        title="My Resource",
        description="This is my resource.",
    ).compact_dict


def test_accepts_well_formed_path(resource_properties):
    """Should accept a set of properties with a well-formed data path."""
    assert verify_data_path(resource_properties) == resource_properties


def test_rejects_properties_with_no_path(resource_properties):
    """Given a set of properties without a data path, should throw
    NotPropertiesError."""
    del resource_properties["path"]

    with raises(
        NotPropertiesError,
        match="No resource ID found",
    ):
        verify_data_path(resource_properties)


@mark.parametrize(
    "data_path",
    [
        Path("resources", "x", "data.parquet"),
        Path("1", "data.parquet"),
        Path("resources", "1", "data.parquet", "1"),
    ],
)
def test_rejects_malformed_path(resource_properties, data_path):
    """Given a set of properties with a malformed data path, should throw
    NotPropertiesError."""
    resource_properties["path"] = str(data_path)

    with raises(
        NotPropertiesError,
        match="No resource ID found",
    ):
        verify_data_path(resource_properties)
