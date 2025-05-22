from jsonschema import SchemaError
from pytest import raises

from seedcase_sprout.check_datapackage.check_object_against_json_schema import (
    check_object_against_json_schema,
)

schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "pattern": "^[a-z0-9]+$",
            "description": "Unique identifier for the object.",
        },
        "title": {
            "type": "string",
            "description": "Title of the entity.",
        },
        "created_at": {
            "type": "string",
            "format": "date-time",
            "description": "Timestamp when the entity was created.",
        },
        "tags": {
            "type": "array",
            "items": {"type": "string", "description": "A tag for the item."},
            "description": "List of tags for categorisation",
        },
    },
    "required": ["id", "title", "created_at"],
}


def test_passes_matching_object():
    """Should pass an object matching the schema."""
    instance = {
        "id": "abc123",
        "title": "a title",
        "created_at": "2024-05-14T05:00:01+00:00",
        "tags": ["a", "b", "c"],
    }

    assert check_object_against_json_schema(instance, schema) == []


def test_fails_instance_with_missing_required_fields():
    """Should fail an object with missing required fields."""
    errors = check_object_against_json_schema({}, schema)

    assert len(errors) == len(schema["required"])
    assert all(error.validator == "required" for error in errors)


def test_fails_instance_with_bad_type():
    """Should fail an object with a field of the wrong type."""
    instance = {
        "id": 123,
        "title": "a title",
        "created_at": "2024-05-14T05:00:01+00:00",
    }

    errors = check_object_against_json_schema(instance, schema)

    assert len(errors) == 1
    assert errors[0].validator == "type"
    assert errors[0].json_path == "$.id"


def test_fails_instance_with_bad_format():
    """Should fail an object with a field of the wrong format."""
    instance = {
        "id": "abc123",
        "title": "a title",
        "created_at": "bad date",
    }

    errors = check_object_against_json_schema(instance, schema)

    assert len(errors) == 1
    assert errors[0].validator == "format"
    assert errors[0].json_path == "$.created_at"


def test_fails_instance_with_pattern_mismatch():
    """Should fail an object with a field that does not match the pattern."""
    instance = {
        "id": "space in id",
        "title": "a title",
        "created_at": "2024-05-14T05:00:01+00:00",
    }

    errors = check_object_against_json_schema(instance, schema)

    assert len(errors) == 1
    assert errors[0].validator == "pattern"
    assert errors[0].json_path == "$.id"


def test_fails_bad_schema():
    """Should raise SchemaError when given an incorrect schema."""
    bad_schema = {"type": "object", "required": "not an array"}

    with raises(SchemaError):
        check_object_against_json_schema({}, bad_schema)
