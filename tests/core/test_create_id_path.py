from seedcase_sprout.core.create_id_path import create_id_path


def test_return_the_resource_path(tmp_path):
    """Return the resource path."""
    assert create_id_path(tmp_path, 1) == tmp_path / "1"
