"""Tests for check_is_image_file."""

from pathlib import Path

from functions.check_is_image_file import check_is_image_file


def test_check_is_image_file_returns_expected_values(tmp_path: Path) -> None:
    """It should detect supported image files and reject others."""
    image_path = tmp_path / "photo.JPG"
    image_path.write_bytes(b"fake-image-content")

    text_path = tmp_path / "notes.txt"
    text_path.write_text("not an image", encoding="utf-8")

    assert check_is_image_file(image_path)
    assert not check_is_image_file(text_path)
