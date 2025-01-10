from pathlib import Path

from seedcase_sprout.core.path_sprout_global import path_sprout_global


def test_returns_global_envvar_if_set(monkeypatch):
    """Returns Sprout's global path when SPROUT_GLOBAL is set."""
    # Given
    SPROUT_GLOBAL = "my/sprout/global"
    monkeypatch.setenv("SPROUT_GLOBAL", SPROUT_GLOBAL)

    # When
    path_global = path_sprout_global()

    # Then
    assert path_global == Path(SPROUT_GLOBAL)
    assert path_global.name == "global"


def test_returns_global_path_when_SPROUT_GLOBAL_is_not_set():
    """Returns Sprout's global path when SPROUT_GLOBAL isn't set."""
    assert path_sprout_global().name == "sprout"
