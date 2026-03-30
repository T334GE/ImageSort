"""Collect image paths from folders and/or direct image file paths."""

from pathlib import Path
from typing import Iterable

from functions.check_is_image_file import check_is_image_file


def get_image_paths_from_source_paths(source_paths: Iterable[str]) -> list[str]:
    """Resolve image paths from source paths.

    Each source path must be either:
    - a folder (searched recursively)
    - a supported image file
    """
    image_paths: set[str] = set()

    for source_path in source_paths:
        path = Path(source_path)

        if path.is_dir():
            for file_path in path.rglob("*"):
                if check_is_image_file(file_path):
                    image_paths.add(str(file_path.resolve()))
            continue

        if check_is_image_file(path):
            image_paths.add(str(path.resolve()))
            continue

        raise ValueError(
            f"Source path must be a folder or supported image file: {path}"
        )

    return sorted(image_paths)
