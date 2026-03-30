"""Tests for copy_images_to_category."""

from pathlib import Path

from functions.copy_images_to_category import copy_images_to_category


def test_copy_images_to_category_copies_files_and_avoids_collisions(tmp_path: Path) -> None:
    """It should copy files and rename duplicates with incremented suffixes."""
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

    copied_paths = copy_images_to_category(
        [str(first_image), str(second_image)],
        str(category_folder),
    )

    assert first_image.exists()
    assert second_image.exists()

    copied_names = sorted(Path(path).name for path in copied_paths)
    assert copied_names == ["image.jpg", "image_1.jpg"]
