from pathlib import Path

from frictionless import errors
from pytest import fixture, mark, raises

from sprout.core.not_properties_error import NotPropertiesError
from sprout.core.properties import (
    PackageProperties,
    ResourceProperties,
    TableSchemaProperties,
)
from sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)

package_error = errors.PackageError.type
resource_error = errors.ResourceError.type


@fixture
def package_properties():
    return PackageProperties(
        name="my-package",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="2.0.0",
        created="2024-05-14T05:00:01+00:00",
    ).asdict


@fixture
def resource_properties() -> dict:
    return ResourceProperties(
        name="my-resource",
        path=str(Path("resources", "1", "data.parquet")),
        title="My Resource",
        description="This is my resource.",
    ).asdict


@mark.parametrize(
    "properties_cls, error_type",
    [
        (PackageProperties, package_error),
        (ResourceProperties, resource_error),
    ],
)
def test_accepts_default_values(properties_cls, error_type):
    """Should accept an object with default values, some of which are blank."""
    properties = properties_cls().asdict

    assert verify_properties_are_well_formed(properties, error_type) == properties


@mark.parametrize(
    "properties, error_type",
    [
        ("package_properties", package_error),
        ("resource_properties", resource_error),
    ],
)
def test_accepts_custom_values(properties, error_type, request):
    """Should accept a well-formed properties object."""
    properties = request.getfixturevalue(properties)

    assert verify_properties_are_well_formed(properties, error_type) == properties


@mark.parametrize(
    "properties, error_type",
    [
        ("package_properties", package_error),
        ("resource_properties", resource_error),
    ],
)
def test_rejects_properties_not_conforming_to_spec(properties, error_type, request):
    """Should reject an object with a value not meeting the Data Package spec."""
    properties = request.getfixturevalue(properties)
    properties["name"] = "an invalid name with spaces"

    with raises(NotPropertiesError, match="at property 'name'"):
        verify_properties_are_well_formed(properties, error_type)


def test_filters_for_package_errors(package_properties):
    """Should throw only if PackageErrors are detected."""
    bad_resource = ResourceProperties(name="a bad name with spaces").asdict
    package_properties["resources"].append(bad_resource)

    assert (
        verify_properties_are_well_formed(package_properties, package_error)
        == package_properties
    )


def test_filters_for_resource_errors(resource_properties):
    """Should throw only if ResourceErrors are detected."""
    bad_schema = TableSchemaProperties(fields="these are not fields").asdict
    resource_properties["schema"] = bad_schema

    assert (
        verify_properties_are_well_formed(resource_properties, resource_error)
        == resource_properties
    )
