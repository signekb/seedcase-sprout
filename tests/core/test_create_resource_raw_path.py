from sprout.core.create_resource_raw_path import create_resource_raw_path


def test_outputs_correct_raw_directory_path(tmp_path):
    """The raw directory path is output correctly."""
    assert create_resource_raw_path(tmp_path) == tmp_path / "raw"
