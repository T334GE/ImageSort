"""Tests for remove_image_files."""

from pathlib import Path

import pytest

from functions.remove_image_files import remove_image_files


def test_remove_image_files_deletes_files_and_returns_paths(tmp_path: Path) -> None:
    """It should delete files and return resolved paths."""
    first_image = tmp_path / "first.jpg"
    second_image = tmp_path / "second.jpg"
    first_image.write_bytes(b"one")
    second_image.write_bytes(b"two")

    removed_paths = remove_image_files([str(first_image), str(second_image)])

    assert not first_image.exists()
    assert not second_image.exists()
    assert sorted(removed_paths) == sorted(
        [str(first_image.resolve()), str(second_image.resolve())]
    )


def test_remove_image_files_raises_for_missing_file(tmp_path: Path) -> None:
    """It should raise an error when any file path is missing."""
    missing_image = tmp_path / "missing.jpg"

    with pytest.raises(FileNotFoundError):
        remove_image_files([str(missing_image)])
