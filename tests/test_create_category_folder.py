"""Tests for create_category_folder."""

from pathlib import Path

from functions.create_category_folder import create_category_folder


def test_create_category_folder_creates_directory(tmp_path: Path) -> None:
    """It should create a category folder in the destination root."""
    created_path = create_category_folder(str(tmp_path), "  Pets  ")

    category_path = Path(created_path)
    assert category_path.is_dir()
    assert category_path.name == "Pets"
