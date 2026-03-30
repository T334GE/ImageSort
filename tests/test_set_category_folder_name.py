"""Tests for set_category_folder_name."""

from pathlib import Path

import pytest

from functions.set_category_folder_name import set_category_folder_name


def test_set_category_folder_name_renames_directory(tmp_path: Path) -> None:
    """It should rename the category folder and return the new absolute path."""
    source_path = tmp_path / "Animals"
    source_path.mkdir()

    renamed_path = Path(set_category_folder_name(str(source_path), "Pets"))

    assert renamed_path.is_dir()
    assert renamed_path.name == "Pets"
    assert not source_path.exists()


def test_set_category_folder_name_raises_if_target_exists(tmp_path: Path) -> None:
    """It should fail when the target category name already exists."""
    source_path = tmp_path / "Animals"
    source_path.mkdir()
    (tmp_path / "Pets").mkdir()

    with pytest.raises(FileExistsError):
        set_category_folder_name(str(source_path), "Pets")
