from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine

from sprout.core.get_iso_timestamp import get_iso_timestamp


@time_machine.travel(datetime(2024, 5, 14, 5, 0, 1), tick=False)
def test_formats_timestamp_in_utc_correctly():
    """Should return a correctly formatted timestamp in the default timezone."""
    assert get_iso_timestamp() == "2024-05-14T05:00:01+00:00"


@time_machine.travel(
    datetime(2024, 5, 14, 5, 0, 1, tzinfo=ZoneInfo("Europe/Copenhagen")), tick=False
)
def test_formats_timestamp_in_other_timezone_correctly():
    """Should return a correctly formatted timestamp in a specific timezone."""
    assert get_iso_timestamp() == "2024-05-14T05:00:01+02:00"
