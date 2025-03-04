from re import escape

from pytest import fixture, mark, raises

from seedcase_sprout.core import (
    path_package,
    path_packages,
    path_properties,
    path_readme,
)
from tests.core.directory_structure_setup import (
    create_test_package_structure,
)


# Given one package
@fixture
def tmp_sprout_global(monkeypatch, tmp_path):
    """Set up test package folder structure and return temp global directory"""
    monkeypatch.setenv("SPROUT_GLOBAL", str(tmp_path))
    create_test_package_structure(tmp_path, "1")

    return tmp_path


@mark.parametrize(
    "function, expected_path",
    [
        (path_package, "packages/1"),
        (path_properties, "packages/1/datapackage.json"),
        (path_readme, "packages/1/README.md"),
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
    [path_package, path_properties, path_readme],
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
