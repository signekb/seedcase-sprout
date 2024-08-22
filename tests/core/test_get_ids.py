from sprout.core.get_ids import get_ids, get_number_from_dir


def test_get_single_id(tmp_path):
    """Return a list of a single ID/integer."""
    (tmp_path / "1").mkdir()
    assert get_ids(tmp_path) == [1]


def test_get_only_dirs(tmp_path):
    """Return only directories - not files."""
    (tmp_path / "1").mkdir()
    (tmp_path / "datapackage.json").touch()
    (tmp_path / "1.txt").touch()
    (tmp_path / "2").touch()

    assert get_ids(tmp_path) == [1]


def test_empty_list_when_no_ids(tmp_path):
    """Return an empty list when there are no IDs."""
    assert get_ids(tmp_path) == []


def test_return_multiple_ids(tmp_path):
    """Return multiple IDs."""
    (tmp_path / "1").mkdir()
    (tmp_path / "2").mkdir()

    assert sorted(get_ids(tmp_path)) == [1, 2]


def test_return_only_id_dirs(tmp_path):
    """Return only directories with IDs/numbers only."""
    (tmp_path / "1").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "1a").mkdir()
    (tmp_path / "b3").mkdir()

    assert get_ids(tmp_path) == [1]


def test_different_numbers_output(tmp_path):
    """Return numbers of any size."""
    (tmp_path / "1").mkdir()
    (tmp_path / "20").mkdir()
    (tmp_path / "999").mkdir()

    assert sorted(get_ids(tmp_path)) == [1, 20, 999]


def test_get_number_from_dir_returns_number(tmp_path):
    """get_number_from_dir() returns only the number from a directory ."""
    assert get_number_from_dir(tmp_path / "1") == 1


def test_get_number_from_dir_returns_none(tmp_path):
    """get_number_from_dir() returns None when the directory name is not an
    ID/a number."""
    assert get_number_from_dir(tmp_path / "b1") is None
