from sprout.core.create_readme_path import create_readme_path


def test_returns_path_to_readme(tmp_path):
    """Given a folder, should return the correct path to the README."""
    assert create_readme_path(tmp_path) == tmp_path / "README.md"
