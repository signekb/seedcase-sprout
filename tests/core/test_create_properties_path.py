from sprout.core.create_properties_path import create_properties_path


def test_returns_path_to_datapackage_file(tmp_path):
    """Given a path to a package, should return the path to the datapackage.json of
    the package."""
    assert create_properties_path(tmp_path) == tmp_path / "datapackage.json"
