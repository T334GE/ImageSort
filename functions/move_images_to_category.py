"""Move image files into a selected category folder."""

import shutil
from pathlib import Path
from typing import Iterable

from functions.get_app_logger import get_app_logger
from functions.get_available_file_path import get_available_file_path


def move_images_to_category(image_paths: Iterable[str], category_path: str) -> list[str]:
    """Move image_paths into category_path and return final destination paths."""
    logger = get_app_logger()
    category = Path(category_path)
    if not category.is_dir():
        logger.log_warning(f"Move target category does not exist: {category}")
        raise NotADirectoryError(f"Category folder does not exist: {category}")

    logger.log_info(f"Moving images to category '{category.resolve()}'.")

    moved_paths: list[str] = []

    for image_path in image_paths:
        source_path = Path(image_path)
        if not source_path.is_file():
            logger.log_warning(f"Move source file does not exist: {source_path}")
            raise FileNotFoundError(f"Image file does not exist: {source_path}")

        destination_path = get_available_file_path(category, source_path.name)
        try:
            final_path = Path(shutil.move(str(source_path), str(destination_path))).resolve()
        except Exception:
            logger.log_exception(
                f"Failed moving '{source_path}' to '{destination_path}'."
            )
            raise

        logger.log_info(f"Moved '{source_path}' to '{final_path}'.")
        moved_paths.append(str(final_path))

    logger.log_info(f"Moved {len(moved_paths)} image(s) to '{category.resolve()}'.")
    return moved_paths
