from dataclasses import asdict
from uuid import uuid4

from sprout.core.get_iso_timestamp import get_iso_timestamp
from sprout.core.properties import PackageProperties


def create_default_package_properties() -> dict:
    """Creates a `PackageProperties` object with default values.

    Returns:
        A dictionary representation of the package properties.
    """
    package_properties = PackageProperties(
        id=str(uuid4()),
        version="0.1.0",
        created=get_iso_timestamp(),
    )
    return asdict(package_properties)
