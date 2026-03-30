"""Tests for get_available_file_path."""

from pathlib import Path

from functions.get_available_file_path import get_available_file_path


def test_get_available_file_path_returns_incremented_name(tmp_path: Path) -> None:
    """It should generate an incremented file name when a conflict exists."""
    (tmp_path / "photo.jpg").write_bytes(b"img")
    (tmp_path / "photo_1.jpg").write_bytes(b"img")

    available_path = get_available_file_path(tmp_path, "photo.jpg")

    assert available_path.name == "photo_2.jpg"
