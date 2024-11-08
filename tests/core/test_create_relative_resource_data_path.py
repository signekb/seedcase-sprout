from pathlib import Path

from seedcase_sprout.core.create_relative_resource_data_path import (
    create_relative_resource_data_path,
)


def test_returns_relative_path_with_single_digits(tmp_path):
    """Return the relative data path when package and resource ID are single digits."""
    tmp_path = tmp_path / "packages" / "1" / "resources" / "1"
    relative_path = Path("resources") / "1"

    assert (
        create_relative_resource_data_path(tmp_path) == relative_path / "data.parquet"
    )


def test_returns_relative_path_with_multi_digits(tmp_path):
    """Return the relative data path when package and resource ID are multi-digits."""
    tmp_path = tmp_path / "packages" / "100" / "resources" / "100"
    relative_path = Path("resources") / "100"

    assert (
        create_relative_resource_data_path(tmp_path) == relative_path / "data.parquet"
    )
