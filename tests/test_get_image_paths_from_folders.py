"""Tests for get_image_paths_from_folders."""

from pathlib import Path

from functions.get_image_paths_from_folders import get_image_paths_from_folders


def test_get_image_paths_from_folders_collects_images_recursively(tmp_path: Path) -> None:
    """It should recursively collect supported image files from a folder."""
    source_folder = tmp_path / "source"
    nested_folder = source_folder / "nested"
    nested_folder.mkdir(parents=True)

    first_image = source_folder / "a.jpg"
    first_image.write_bytes(b"img-a")

    second_image = nested_folder / "b.png"
    second_image.write_bytes(b"img-b")

    ignored_file = nested_folder / "readme.md"
    ignored_file.write_text("ignore me", encoding="utf-8")

    image_paths = get_image_paths_from_folders([str(source_folder)])

    assert image_paths == sorted(
        [
            str(first_image.resolve()),
            str(second_image.resolve()),
        ]
    )
