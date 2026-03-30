"""Collect image paths recursively from folders."""

from pathlib import Path
from typing import Iterable

from functions.check_is_image_file import check_is_image_file


def get_image_paths_from_folders(folder_paths: Iterable[str]) -> list[str]:
    """Get all supported image file paths recursively from folder_paths."""
    image_paths: set[str] = set()

    for folder_path in folder_paths:
        folder = Path(folder_path)
        if not folder.is_dir():
            raise NotADirectoryError(f"Folder does not exist: {folder}")

        for file_path in folder.rglob("*"):
            if check_is_image_file(file_path):
                image_paths.add(str(file_path.resolve()))

    return sorted(image_paths)
