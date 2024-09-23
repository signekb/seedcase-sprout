from pytest import raises

from sprout.core.write_json import write_json


def test_writes_dictionary_to_json_correctly(tmp_path):
    """Given a path and a dictionary, should write the dictionary to the path as
    correctly indented JSON and return the path."""
    # given
    file_path_in = tmp_path / "test.test"
    json_object = {
        "outer": "value",
        "inner": {"prop1": 123, "prop2": [1, 2, None], "prop3": True},
    }
    expected_contents = (
        "{\n"
        '  "outer": "value",\n'
        '  "inner": {\n'
        '    "prop1": 123,\n'
        '    "prop2": [\n'
        "      1,\n"
        "      2,\n"
        "      null\n"
        "    ],\n"
        '    "prop3": true\n'
        "  }\n"
        "}"
    )

    # when
    file_path_out = write_json(json_object, file_path_in)

    # then
    assert file_path_out == file_path_in
    assert file_path_out.is_file()
    assert file_path_out.read_text() == expected_contents


def test_writes_list_to_json_correctly(tmp_path):
    """Given a path and a list, should write the list to the path as correctly
    indented JSON and return the path."""
    # given
    file_path_in = tmp_path / "test.test"
    json_object = [{"prop1": "value"}, {"prop2": 123}]
    expected_contents = (
        "[\n"
        "  {\n"
        '    "prop1": "value"\n'
        "  },\n"
        "  {\n"
        '    "prop2": 123\n'
        "  }\n"
        "]"
    )

    # when
    file_path_out = write_json(json_object, file_path_in)

    # then
    assert file_path_out == file_path_in
    assert file_path_out.is_file()
    assert file_path_out.read_text() == expected_contents


def test_rejects_invalid_object(tmp_path):
    """Given an object which is not JSON serialisable, should throw TypeError."""
    invalid_object = {"path": tmp_path}

    with raises(TypeError):
        write_json(invalid_object, tmp_path / "test.test")


def test_rejects_path_with_nonexistent_parent_folder(tmp_path):
    """Given a path with a nonexistent parent, should throw FileNotFoundError."""
    with raises(FileNotFoundError):
        write_json({}, tmp_path / "nonexistent" / "test.test")
