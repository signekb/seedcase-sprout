from uuid import uuid4

from seedcase_sprout.core.get_iso_timestamp import get_iso_timestamp
from seedcase_sprout.core.properties import (
    ContributorProperties,
    FieldProperties,
    LicenseProperties,
    PackageProperties,
    ResourceProperties,
    TableSchemaProperties,
)


def example_package_properties() -> PackageProperties:
    """Generate an example package properties object.

    Returns:
        Outputs a correctly formatted example `PackageProperties` object.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp
        sp.example_package_properties()
        ```
    """
    properties = PackageProperties(
        name="example-package",
        version="0.1.0",
        created=get_iso_timestamp(),
        id=str(uuid4()),
        title="Example fake data package",
        description="Data from a fake data package on something.",
        contributors=[
            ContributorProperties(
                title="Jamie Jones",
                email="jamie_jones@example.com",
                roles=["creator"],
            )
        ],
        licenses=[
            LicenseProperties(
                name="ODC-BY-1.0",
                path="https://opendatacommons.org/licenses/by",
                title="Open Data Commons Attribution License 1.0",
            )
        ],
    )

    return properties


def example_resource_properties() -> ResourceProperties:
    """Generate an example resource properties object.

    Returns:
        Outputs a correctly formatted example `ResourceProperties` object.

    Examples:
        ```{python}
        import seedcase_sprout.core as sp
        sp.example_resource_properties()
        ```
    """
    return ResourceProperties(
        name="example-resource",
        title="Example fake data resource",
        description="Data from a fake resource on something.",
        path="resources/1/data.parquet",
        schema=TableSchemaProperties(
            fields=[
                FieldProperties(
                    name="id",
                    title="ID",
                    description="Unique identifier for the record.",
                    type="integer",
                ),
                FieldProperties(
                    name="name",
                    title="Name",
                    description="Name of the record.",
                    type="string",
                ),
                FieldProperties(
                    name="value",
                    title="Value",
                    description="Value of the record.",
                    type="number",
                ),
            ]
        ),
    )
