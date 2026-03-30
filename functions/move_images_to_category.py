"""Move image files into a selected category folder."""

import shutil
from pathlib import Path
from typing import Iterable

from functions.get_available_file_path import get_available_file_path


def move_images_to_category(image_paths: Iterable[str], category_path: str) -> list[str]:
    """Move image_paths into category_path and return final destination paths."""
    category = Path(category_path)
    if not category.is_dir():
        raise NotADirectoryError(f"Category folder does not exist: {category}")

    moved_paths: list[str] = []

    for image_path in image_paths:
        source_path = Path(image_path)
        if not source_path.is_file():
            raise FileNotFoundError(f"Image file does not exist: {source_path}")

        destination_path = get_available_file_path(category, source_path.name)
        final_path = Path(shutil.move(str(source_path), str(destination_path))).resolve()
        moved_paths.append(str(final_path))

    return moved_paths
