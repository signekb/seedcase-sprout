from pathlib import Path

from seedcase_sprout.core.get_root_envvar import get_root_envvar


def test_returns_root_envvar_if_set(monkeypatch):
    """Returns SPROUT_ROOT if it is set."""
    # Given
    SPROUT_ROOT = "my/sprout/root"
    monkeypatch.setenv("SPROUT_ROOT", SPROUT_ROOT)

    # When, then
    assert get_root_envvar() == Path(SPROUT_ROOT)


def test_returns_none_if_root_envvar_is_not_set():
    """Returns None if SPROUT_ROOT isn't set."""
    assert get_root_envvar() is None
