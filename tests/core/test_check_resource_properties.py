from seedcase_sprout.core.checks.check_resource_properties import (
    check_resource_properties,
)

# Without recommendations


def test_passes_matching_properties():
    """Should pass properties matching the schema."""
    properties = {"name": "a name with spaces", "path": "data.csv"}

    assert check_resource_properties(properties, check_recommendations=False) == []


def test_fails_properties_with_missing_required_fields():
    """Should fail properties with missing required fields."""
    errors = check_resource_properties({}, check_recommendations=False)

    assert len(errors) == 1
    assert errors[0].validator == "oneOf"
    assert errors[0].json_path == "$"

    context = errors[0].context
    assert len(context) == 4
    assert all(error.validator == "required" for error in context)


def test_fails_properties_with_bad_type():
    """Should fail properties with a field of the wrong type."""
    properties = {"name": 123, "path": "data.csv"}

    errors = check_resource_properties(properties, check_recommendations=False)

    assert len(errors) == 1
    assert errors[0].validator == "type"
    assert errors[0].json_path == "$.name"


def test_fails_properties_with_bad_format():
    """Should fail properties with a field of the wrong format."""
    properties = {"name": "name", "path": "data.csv", "homepage": "not a URL"}

    errors = check_resource_properties(properties, check_recommendations=False)

    assert len(errors) == 1
    assert errors[0].validator == "format"
    assert errors[0].json_path == "$.homepage"


def test_fails_properties_with_pattern_mismatch():
    """Should fail properties with a field that does not match the pattern."""
    properties = {"name": "a name with spaces", "path": "/bad/path.csv"}

    errors = check_resource_properties(properties, check_recommendations=False)

    assert len(errors) == 1
    assert errors[0].validator == "oneOf"
    assert errors[0].json_path == "$.path"
    assert any(error.validator == "pattern" for error in errors[0].context)


# With recommendations


def test_passes_matching_properties_with_recommendations():
    """Should pass properties matching recommendations."""
    properties = {"name": "a-name-with-no-spaces", "path": "data.csv"}

    assert check_resource_properties(properties, check_recommendations=True) == []


def test_fails_properties_with_pattern_mismatch_with_recommendations():
    """Should fail properties with field violating recommendations."""
    properties = {"name": "a name with spaces", "path": "data.csv"}

    errors = check_resource_properties(properties, check_recommendations=True)

    assert len(errors) == 1
    assert errors[0].validator == "pattern"
    assert errors[0].json_path == "$.name"
