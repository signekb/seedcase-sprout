import os

from seedcase_sprout.core import PackagePath


def test_package_path_outputs_an_absolute_path(tmp_path):
    """Test that the path functions output an absolute path."""
    # This is a simple test to just check that a path is output.
    # Need to give the `tmp_path` to the class otherwise it uses the working directory
    # of the test script.
    path = PackagePath(tmp_path)
    assert path.properties().is_absolute()
    assert path.readme().is_absolute()
    assert path.resources().is_absolute()
    assert path.resource("test").is_absolute()
    assert path.resource_data("test").is_absolute()
    assert path.resource_batch("test").is_absolute()
    # TODO: Test `resource_batch_files()` after deciding whether to do a check first?


def test_path_defaults_to_cwd_at_call_time(tmp_path):
    """When no root path is provided, the root path should default to the cwd of the
    calling script."""
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        package_path = PackagePath()
        assert package_path.path == tmp_path
    finally:
        os.chdir(original_cwd)
