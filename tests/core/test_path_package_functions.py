from re import escape

from pytest import fixture, mark, raises

from sprout.core import (
    path_package,
    path_package_database,
    path_package_properties,
    path_packages,
)
from tests.core.directory_structure_setup import (
    create_test_package_structure,
)


# Given one package
@fixture
def tmp_sprout_root(monkeypatch, tmp_path):
    """Set up test package folder structure and return temp root directory"""
    monkeypatch.setenv("SPROUT_ROOT", str(tmp_path))
    create_test_package_structure(tmp_path, "1")

    return tmp_path


@mark.parametrize(
    "function, expected_path",
    [
        (path_package, "packages/1"),
        (path_package_database, "packages/1/database.sql"),
        (path_package_properties, "packages/1/datapackage.json"),
    ],
)
def test_path_package_functions_return_expected_path(
    tmp_sprout_root, function, expected_path
):
    # When, then
    assert function(package_id=1) == tmp_sprout_root / expected_path
    assert function(package_id=1).is_file() or function(package_id=1).is_dir()


@mark.parametrize(
    "function",
    [path_package, path_package_database, path_package_properties],
)
def test_path_package_functions_raise_error_if_package_id_does_not_exist(
    tmp_sprout_root, function
):
    # When, then
    with raises(NotADirectoryError, match=escape("[1]")):
        function(package_id=2)


def test_path_packages_returns_expected_path(tmp_sprout_root):
    # When, then
    assert path_packages() == tmp_sprout_root / "packages"


def test_path_packages_creates_and_returns_expected_path_when_no_packages_exist(
    monkeypatch, tmp_path
):
    # When
    monkeypatch.setenv("SPROUT_ROOT", str(tmp_path))

    # Then
    assert path_packages() == tmp_path / "packages"
    assert path_packages().is_dir()
