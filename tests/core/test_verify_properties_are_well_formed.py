from frictionless import errors
from pytest import fixture, raises

from sprout.core.not_properties_error import NotPropertiesError
from sprout.core.properties import PackageProperties, ResourceProperties
from sprout.core.verify_properties_are_well_formed import (
    verify_properties_are_well_formed,
)

package_error = errors.PackageError.type


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


def test_accepts_default_values():
    """Should accept an object with default values, some of which are blank."""
    properties = PackageProperties().asdict

    assert verify_properties_are_well_formed(properties, package_error) == properties


def test_accepts_custom_values(package_properties):
    """Should accept a well-formed properties object."""
    assert (
        verify_properties_are_well_formed(package_properties, package_error)
        == package_properties
    )


def test_rejects_properties_not_conforming_to_spec(package_properties):
    """Should reject an object with a value not meeting the Data Package spec."""
    package_properties["name"] = "an invalid name with spaces"

    with raises(NotPropertiesError, match="at property 'name'"):
        verify_properties_are_well_formed(package_properties, package_error)


def test_filters_for_the_specified_error_type(package_properties):
    """Should throw only if PackageErrors are detected."""
    bad_resource = ResourceProperties(name="a bad name with spaces").asdict
    package_properties["resources"].append(bad_resource)

    assert (
        verify_properties_are_well_formed(package_properties, package_error)
        == package_properties
    )
