from pathlib import Path

from seedcase_sprout.core.get_global_envvar import get_global_envvar


def test_returns_global_envvar_if_set(monkeypatch):
    """Returns SPROUT_GLOBAL if it is set."""
    # Given
    SPROUT_GLOBAL = "my/sprout/global"
    monkeypatch.setenv("SPROUT_GLOBAL", SPROUT_GLOBAL)

    # When, then
    assert get_global_envvar() == Path(SPROUT_GLOBAL)


def test_returns_none_if_global_envvar_is_not_set():
    """Returns None if SPROUT_GLOBAL isn't set."""
    assert get_global_envvar() is None
