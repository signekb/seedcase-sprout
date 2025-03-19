from datetime import datetime
from unittest.mock import patch
from uuid import UUID
from zoneinfo import ZoneInfo

import time_machine

from seedcase_sprout.core.create_batch_file_name import create_batch_file_name


@patch("seedcase_sprout.core.create_batch_file_name.uuid4", return_value=UUID(int=1))
@time_machine.travel(datetime(2024, 5, 14, 5, 0, 1, tzinfo=ZoneInfo("UTC")), tick=False)
def test_returns_expected_batch_file_name(mock_uuid):
    file_name = create_batch_file_name()

    assert file_name == f"2024-05-14T050001Z-{mock_uuid()}"
