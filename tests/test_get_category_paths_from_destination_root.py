"""Tests for get_category_paths_from_destination_root."""

from pathlib import Path

import pytest

from functions.get_category_paths_from_destination_root import (
    get_category_paths_from_destination_root,
)


def test_get_category_paths_from_destination_root_returns_sorted_folders(
    tmp_path: Path,
) -> None:
    """It should return only child folders sorted by category name."""
    (tmp_path / "zebra").mkdir()
    (tmp_path / "Alpha").mkdir()
    (tmp_path / "notes.txt").write_text("ignore", encoding="utf-8")

    category_paths = get_category_paths_from_destination_root(str(tmp_path))

    assert [Path(path).name for path in category_paths] == ["Alpha", "zebra"]


def test_get_category_paths_from_destination_root_raises_for_missing_directory(
    tmp_path: Path,
) -> None:
    """It should fail when the destination root does not exist."""
    missing_directory = tmp_path / "missing"

    with pytest.raises(NotADirectoryError):
        get_category_paths_from_destination_root(str(missing_directory))
