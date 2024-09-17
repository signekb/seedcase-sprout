from pathlib import Path

from sprout.core.path_sprout_root import path_sprout_root


def test_returns_root_envvar_if_set(monkeypatch):
    """Returns Sprout's root path when SPROUT_ROOT is set."""
    # Given
    SPROUT_ROOT = "my/sprout/root"
    monkeypatch.setenv("SPROUT_ROOT", SPROUT_ROOT)

    # When
    path_root = path_sprout_root()

    # Then
    assert path_root == Path(SPROUT_ROOT)
    assert path_root.name == "root"


def test_returns_root_path_when_SPROUT_ROOT_is_not_set():
    """Returns Sprout's root path when SPROUT_ROOT isn't set."""
    assert path_sprout_root().name == "sprout"
