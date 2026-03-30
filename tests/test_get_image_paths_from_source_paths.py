"""Tests for get_image_paths_from_source_paths."""

from pathlib import Path

import pytest

from functions.get_image_paths_from_source_paths import get_image_paths_from_source_paths


def test_get_image_paths_from_source_paths_handles_folders_and_images(tmp_path: Path) -> None:
    """It should resolve images from mixed source types without duplicates."""
    folder_path = tmp_path / "album"
    nested_path = folder_path / "nested"
    nested_path.mkdir(parents=True)

    folder_image = nested_path / "a.jpg"
    folder_image.write_bytes(b"a")

    direct_image = tmp_path / "b.png"
    direct_image.write_bytes(b"b")

    image_paths = get_image_paths_from_source_paths(
        [
            str(folder_path),
            str(direct_image),
            str(direct_image),
        ]
    )

    assert image_paths == sorted(
        [
            str(folder_image.resolve()),
            str(direct_image.resolve()),
        ]
    )


def test_get_image_paths_from_source_paths_raises_for_unsupported_path(
    tmp_path: Path,
) -> None:
    """It should fail fast when a source path is neither folder nor image."""
    unsupported_file = tmp_path / "notes.txt"
    unsupported_file.write_text("not image", encoding="utf-8")

    with pytest.raises(ValueError):
        get_image_paths_from_source_paths([str(unsupported_file)])
