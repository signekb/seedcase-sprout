from seedcase_sprout.core.create_root_path import create_root_path


def test_returns_root_path():
    """Returns root path."""
    assert create_root_path().name == "sprout"
