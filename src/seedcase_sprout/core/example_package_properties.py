from seedcase_sprout.core.properties import (
    ContributorProperties,
    LicenseProperties,
    PackageProperties,
)

example_package_properties = PackageProperties(
    name="example-package",
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
