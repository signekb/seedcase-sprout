from dataclasses import asdict

from pytest import mark

from sprout.core.properties import (
    ConstraintsProperties,
    ContributorProperties,
    FieldProperties,
    LicenseProperties,
    MissingValueProperties,
    PackageProperties,
    ReferenceProperties,
    ResourceProperties,
    SourceProperties,
    TableDialectProperties,
    TableSchemaForeignKeyProperties,
    TableSchemaProperties,
)


@mark.parametrize(
    "cls",
    [
        ContributorProperties,
        LicenseProperties,
        SourceProperties,
        TableDialectProperties,
        ReferenceProperties,
        TableSchemaForeignKeyProperties,
        MissingValueProperties,
        ConstraintsProperties,
        FieldProperties,
        TableSchemaProperties,
        ResourceProperties,
        PackageProperties,
    ],
)
def test_asdict_generates_dictionary(cls):
    """Should return a dictionary representation of the object."""
    properties = cls()

    assert properties.asdict == asdict(properties)
