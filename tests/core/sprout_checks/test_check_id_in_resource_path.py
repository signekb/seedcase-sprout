from pathlib import Path

from pytest import mark

from seedcase_sprout.core.sprout_checks.check_id_in_resource_path import (
    check_id_in_resource_path,
)
from seedcase_sprout.core.sprout_checks.get_json_path_to_resource_field import (
    get_json_path_to_resource_field,
)


@mark.parametrize("index", [None, 2])
def test_passes_if_data_path_well_formed(index):
    """Should pass if the path contains a resource ID."""
    properties = {"path": str(Path("resources", "1", "data.parquet"))}

    assert check_id_in_resource_path(properties, index) == []


@mark.parametrize("index", [None, 2])
def test_passes_if_data_path_not_present(index):
    """Should pass if the path is not set."""
    assert check_id_in_resource_path({}, index) == []


@mark.parametrize("index", [None, 2])
@mark.parametrize("data_path", [123, []])
def test_passes_if_path_of_wrong_type(index, data_path):
    """Should pass if path is of the wrong type."""
    properties = {"path": data_path}

    assert check_id_in_resource_path(properties, index) == []


@mark.parametrize("index", [None, 2])
@mark.parametrize(
    "data_path",
    [
        "",
        Path("resources", "x", "data.parquet"),
        Path("1", "data.parquet"),
        Path("resources", "1", "data.parquet", "1"),
    ],
)
def test_returns_error_if_data_path_is_malformed(index, data_path):
    """Returns list of `CheckError`s if the data path does not contain a resource ID."""
    properties = {"path": str(data_path)}

    errors = check_id_in_resource_path(properties, index)

    assert len(errors) == 1
    assert errors[0].message
    assert errors[0].json_path == get_json_path_to_resource_field("path", index)
    assert errors[0].validator == "pattern"
