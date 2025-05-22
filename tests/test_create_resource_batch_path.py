from seedcase_sprout.create_resource_batch_path import create_resource_batch_path


def test_outputs_correct_batch_directory_path(tmp_path):
    """The batch directory path is output correctly."""
    assert create_resource_batch_path(tmp_path) == tmp_path / "batch"
