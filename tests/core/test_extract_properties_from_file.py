import csv
import json

from sprout.core.extract_properties_from_file import extract_properties_from_file


def test_extracts_properties_from_empty_csv(tmp_path):
    """Given an empty CSV file, it should extract resource properties
    with an empty 'fields' array."""
    # given
    file_path = tmp_path / "data.csv"
    file_path.touch()
    expected_properties = {
        "name": "data",
        "type": "table",
        "path": str(file_path),
        "scheme": "file",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "schema": {"fields": []},
    }

    # when + then
    assert extract_properties_from_file(file_path) == expected_properties


def test_extracts_properties_from_complete_csv(tmp_path):
    """Given a non-empty CSV file, it should extract resource properties,
    including field information."""
    # given
    file_path = tmp_path / "data.csv"
    data = [["id", "name", "dob"], [1, "Alice", "2000-09-22"], [2, "Bob", "1996-11-12"]]
    expected_properties = {
        "name": "data",
        "type": "table",
        "path": str(file_path),
        "scheme": "file",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "schema": {
            "fields": [
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
                {"name": "dob", "type": "date"},
            ]
        },
    }

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # when + then
    assert extract_properties_from_file(file_path) == expected_properties


def test_extracts_properties_from_json(tmp_path):
    """Given a JSON file, it should extract resource properties without a schema."""
    # given
    file_path = tmp_path / "data.json"
    data = {"outer": {"inner": {"myList": [1, 2, 3]}, "myNumber": 23}}
    expected_properties = {
        "name": "data",
        "type": "json",
        "path": str(file_path),
        "scheme": "file",
        "format": "json",
        "mediatype": "text/json",
        "encoding": "utf-8",
    }

    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file)

    # when + then
    assert extract_properties_from_file(file_path) == expected_properties
