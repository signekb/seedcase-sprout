from pathlib import Path
from re import escape

from pytest import fixture, mark, raises

from seedcase_sprout.core import (
    path_package,
    path_packages,
    path_sprout_global,
)
from seedcase_sprout.core.path_global import (
    _create_sprout_global_path,
    _get_sprout_global_envvar,
)
from tests.core.directory_structure_setup import (
    create_test_global_data_package,
)


# Given one package
@fixture
def tmp_sprout_global(monkeypatch, tmp_path):
    """Set up test package folder structure and return temp global directory"""
    monkeypatch.setenv("SPROUT_GLOBAL", str(tmp_path))
    create_test_global_data_package(tmp_path, "1")

    return tmp_path


@mark.parametrize(
    "function, expected_path",
    [
        (path_package, "packages/1"),
    ],
)
def test_path_package_functions_return_expected_path(
    tmp_sprout_global, function, expected_path
):
    # When, then
    assert function(package_id=1) == tmp_sprout_global / expected_path
    assert function(package_id=1).is_file() or function(package_id=1).is_dir()


@mark.parametrize(
    "function",
    [path_package],
)
def test_path_package_functions_raise_error_if_package_id_does_not_exist(
    tmp_sprout_global, function
):
    # When, then
    with raises(NotADirectoryError, match=escape("[1]")):
        function(package_id=2)


def test_path_packages_returns_expected_path(tmp_sprout_global):
    # When, then
    assert path_packages() == tmp_sprout_global / "packages"


def test_path_packages_creates_and_returns_expected_path_when_no_packages_exist(
    monkeypatch, tmp_path
):
    # When
    monkeypatch.setenv("SPROUT_GLOBAL", str(tmp_path))

    # Then
    assert path_packages() == tmp_path / "packages"
    assert path_packages().is_dir()


def test_returns_global_envvar_if_set(monkeypatch):
    """Returns Sprout's global path when SPROUT_GLOBAL is set."""
    # Given
    SPROUT_GLOBAL = "my/sprout/global"
    monkeypatch.setenv("SPROUT_GLOBAL", SPROUT_GLOBAL)

    # When
    path_global = path_sprout_global()

    # Then
    assert _get_sprout_global_envvar() == Path(SPROUT_GLOBAL)
    assert path_global == Path(SPROUT_GLOBAL)
    assert path_global.name == "global"


def test_returns_global_path_when_SPROUT_GLOBAL_is_not_set():
    """Returns Sprout's global path when SPROUT_GLOBAL isn't set."""
    assert path_sprout_global().name == "sprout"


def test_returns_global_path():
    """Returns global path."""
    assert _create_sprout_global_path().name == "sprout"


def test_returns_none_if_global_envvar_is_not_set():
    """Returns None if SPROUT_GLOBAL isn't set."""
    assert _get_sprout_global_envvar() is None
