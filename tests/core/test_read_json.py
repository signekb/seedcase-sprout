from json import JSONDecodeError
from pathlib import Path

from pytest import mark, raises

from seedcase_sprout.core.read_json import read_json
from seedcase_sprout.core.write_json import write_json


@mark.parametrize(
    "expected",
    [
        {},
        [],
        {
            "outer": "value",
            "inner": {"prop1": 123, "prop2": [1, 2, None], "prop3": True},
        },
        [{"prop1": "value"}, {"prop2": 123}],
    ],
)
def test_reads_valid_file(tmp_path, expected):
    """Should load the contents of a deserialisable JSON file into an object."""
    tmp_path = tmp_path / "test.json"
    write_json(expected, tmp_path)

    assert read_json(tmp_path) == expected


def test_rejects_empty_file(tmp_path):
    """Should reject an empty file."""
    tmp_path = tmp_path / "test.json"
    tmp_path.touch()

    with raises(JSONDecodeError):
        read_json(tmp_path)


@mark.parametrize("contents", [True, None, "test", {"path": Path("test")}])
def test_rejects_invalid_file(tmp_path, contents):
    """Should reject a file whose contents are not deserialisable as JSON."""
    tmp_path = tmp_path / "test.json"
    tmp_path.write_text(str(contents))

    with raises(JSONDecodeError):
        read_json(tmp_path)
