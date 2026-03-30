"""Tests for check_is_sort_source_path."""

from pathlib import Path

from functions.check_is_sort_source_path import check_is_sort_source_path


def test_check_is_sort_source_path_accepts_folder_and_image(tmp_path: Path) -> None:
    """It should accept folders and supported image files."""
    folder_path = tmp_path / "source"
    folder_path.mkdir()

    image_path = tmp_path / "photo.png"
    image_path.write_bytes(b"img")

    assert check_is_sort_source_path(folder_path)
    assert check_is_sort_source_path(image_path)


def test_check_is_sort_source_path_rejects_non_image_file(tmp_path: Path) -> None:
    """It should reject files that are not supported images."""
    text_path = tmp_path / "notes.txt"
    text_path.write_text("hello", encoding="utf-8")

    assert not check_is_sort_source_path(text_path)
