from seedcase_sprout.core.create_sprout_global_path import create_sprout_globalpath


def test_returns_global_path():
    """Returns global path."""
    assert create_sprout_globalpath().name == "sprout"
