"""Copy image files into a selected category folder."""

import shutil
from pathlib import Path
from typing import Iterable

from functions.get_app_logger import get_app_logger
from functions.get_available_file_path import get_available_file_path


def copy_images_to_category(image_paths: Iterable[str], category_path: str) -> list[str]:
    """Copy image_paths into category_path and return final destination paths."""
    logger = get_app_logger()
    category = Path(category_path)
    if not category.is_dir():
        logger.log_warning(f"Copy target category does not exist: {category}")
        raise NotADirectoryError(f"Category folder does not exist: {category}")

    logger.log_info(f"Copying images to category '{category.resolve()}'.")

    copied_paths: list[str] = []

    for image_path in image_paths:
        source_path = Path(image_path)
        if not source_path.is_file():
            logger.log_warning(f"Copy source file does not exist: {source_path}")
            raise FileNotFoundError(f"Image file does not exist: {source_path}")

        destination_path = get_available_file_path(category, source_path.name)
        try:
            final_path = Path(shutil.copy2(str(source_path), str(destination_path))).resolve()
        except Exception:
            logger.log_exception(
                f"Failed copying '{source_path}' to '{destination_path}'."
            )
            raise

        logger.log_info(f"Copied '{source_path}' to '{final_path}'.")
        copied_paths.append(str(final_path))

    logger.log_info(f"Copied {len(copied_paths)} image(s) to '{category.resolve()}'.")
    return copied_paths
