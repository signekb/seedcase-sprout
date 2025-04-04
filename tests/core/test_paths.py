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
