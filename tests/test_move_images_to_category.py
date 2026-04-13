"""Tests for move_images_to_category."""

from pathlib import Path

import pytest

from functions.move_images_to_category import move_images_to_category


def test_move_images_to_category_moves_files_and_avoids_collisions(tmp_path: Path) -> None:
    """It should move files and rename duplicates with incremented suffixes."""
    source_one = tmp_path / "source_one"
    source_two = tmp_path / "source_two"
    category_folder = tmp_path / "cats"

    source_one.mkdir()
    source_two.mkdir()
    category_folder.mkdir()

    first_image = source_one / "image.jpg"
    first_image.write_bytes(b"one")

    second_image = source_two / "image.jpg"
    second_image.write_bytes(b"two")

    moved_paths = move_images_to_category(
        [str(first_image), str(second_image)],
        str(category_folder),
    )

    assert not first_image.exists()
    assert not second_image.exists()

    moved_names = sorted(Path(path).name for path in moved_paths)
    assert moved_names == ["image.jpg", "image_1.jpg"]


def test_move_images_to_category_raises_for_same_source_folder(tmp_path: Path) -> None:
    """It should reject moving a file into the same folder it already belongs to."""
    category_folder = tmp_path / "cats"
    category_folder.mkdir()

    image_path = category_folder / "image.jpg"
    image_path.write_bytes(b"image-bytes")

    with pytest.raises(ValueError):
        move_images_to_category([str(image_path)], str(category_folder))
