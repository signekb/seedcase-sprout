from pathlib import Path

from pytest import fixture, raises

from seedcase_sprout.core.properties import (
    LicenseProperties,
    PackageProperties,
    ResourceProperties,
)
from seedcase_sprout.core.update_package_properties import update_package_properties


@fixture
def original_properties() -> PackageProperties:
    return PackageProperties(
        name="my-package",
        id="123-abc-123",
        title="My Package",
        description="This is my package.",
        version="1.0.0",
        created="2024-05-14T05:00:01+00:00",
        licenses=[LicenseProperties(name="license")],
    )


def test_updates_only_change_package_properties(original_properties):
    """Should only update package properties and leave unchanged values as is."""
    expected_name = "my-new-package-name"
    updated_properties = update_package_properties(
        original_properties, PackageProperties(name=expected_name)
    )

    assert updated_properties.title == updated_properties.title
    assert updated_properties.name == expected_name


def test_current_properties_must_be_complete(original_properties):
    """The current properties needs to be correct and complete."""
    original_properties.name = None
    expected_name = "added-missed-name"
    with raises(ExceptionGroup):
        update_package_properties(
            original_properties, PackageProperties(name=expected_name)
        )


def test_resources_not_added_from_incoming_properties(original_properties):
    """When current properties have no resources, these should not be added from
    incoming properties."""
    properties_updates = PackageProperties(resources=[ResourceProperties()])

    updated_properties = update_package_properties(
        original_properties, properties_updates
    )

    assert updated_properties.resources == properties_updates.resources


def test_current_resources_not_modified(original_properties):
    """When current properties have resources, these should not be modified."""
    original_properties.resources = [
        ResourceProperties(
            name="resource-1",
            path=str(Path("resources", "1", "data.parquet")),
            title="Resource 1",
            description="A resource.",
        )
    ]
    updated_properties = update_package_properties(
        original_properties, PackageProperties(resources=[])
    )

    assert original_properties.resources == updated_properties.resources


def test_error_if_correct_property_is_incorrect(original_properties):
    """Should give an error if the current property is not correct."""
    original_properties.name = "incorrect name with spaces"
    properties_updates = PackageProperties(name="my-new-package-name")

    with raises(ExceptionGroup) as error_info:
        update_package_properties(original_properties, properties_updates)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "pattern"


def test_error_if_current_properties_has_an_incorrect_resource_property(
    original_properties,
):
    """Should give an error if current property has an incorrect resource property."""
    original_properties.resources = [
        ResourceProperties(
            name="incorrect name with spaces",
            path=str(Path("resources", "1", "data.parquet")),
            title="Resource 1",
            description="A resource.",
        )
    ]
    properties_updates = PackageProperties(name="my-new-package-name")

    with raises(ExceptionGroup) as error_info:
        update_package_properties(original_properties, properties_updates)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.resources[0].name"
    assert errors[0].validator == "pattern"


def test_error_for_incorrect_properties_update(original_properties):
    """Give an error if update to property is incorrect."""
    properties_updates = PackageProperties(name="a name with spaces")

    with raises(ExceptionGroup) as error_info:
        update_package_properties(original_properties, properties_updates)

    errors = error_info.value.exceptions
    assert len(errors) == 1
    assert errors[0].json_path == "$.name"
    assert errors[0].validator == "pattern"


def test_error_for_empty_properties(original_properties):
    """If current properties is empty, there should be an error."""
    with raises(ExceptionGroup):
        update_package_properties(PackageProperties(), original_properties)

    with raises(ExceptionGroup):
        update_package_properties(PackageProperties(), PackageProperties())
