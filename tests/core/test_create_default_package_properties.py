from datetime import datetime
from unittest.mock import patch
from uuid import UUID

import time_machine

from sprout.core.create_default_package_properties import (
    create_default_package_properties,
)


@patch("sprout.core.create_default_package_properties.uuid4", return_value=UUID(int=1))
@time_machine.travel(datetime(2024, 5, 14, 5, 0, 1), tick=False)
def test_creates_properties_dict_with_correct_defaults(mock_uuid):
    """Should return a dictionary of package properties containing default values."""
    properties = create_default_package_properties()

    assert type(properties) is dict
    assert properties["id"] == str(mock_uuid())
    assert properties["version"] == "0.1.0"
    assert properties["created"] == "2024-05-14T05:00:01+00:00"
