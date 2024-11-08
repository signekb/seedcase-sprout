from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import time_machine

from seedcase_sprout.core.create_raw_file_name import create_raw_file_name


@patch("seedcase_sprout.core.create_raw_file_name.uuid4", return_value=UUID(int=1))
@time_machine.travel(datetime(2024, 5, 14, 5, 0, 1), tick=False)
def test_returns_expected_raw_file_name(mock_uuid, tmp_path):
    path = create_raw_file_name(Path(tmp_path) / "test.csv")

    assert path == f"2024-05-14T050001Z-{mock_uuid()}.csv.gz"
