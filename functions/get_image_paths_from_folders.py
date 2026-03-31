"""Collect image paths recursively from folders."""

from pathlib import Path
from typing import Iterable

from functions.check_is_image_file import check_is_image_file
from functions.get_app_logger import get_app_logger


def get_image_paths_from_folders(folder_paths: Iterable[str]) -> list[str]:
    """Get all supported image file paths recursively from folder_paths."""
    logger = get_app_logger()
    normalized_folder_paths = list(folder_paths)
    image_paths: set[str] = set()

    for folder_path in normalized_folder_paths:
        folder = Path(folder_path)
        if not folder.is_dir():
            logger.log_warning(f"Folder does not exist for image discovery: {folder}")
            raise NotADirectoryError(f"Folder does not exist: {folder}")

        logger.log_info(f"Scanning folder for images: {folder.resolve()}")

        for file_path in folder.rglob("*"):
            if check_is_image_file(file_path):
                image_paths.add(str(file_path.resolve()))

    sorted_paths = sorted(image_paths)
    logger.log_info(
        f"Collected {len(sorted_paths)} image file(s) from {len(normalized_folder_paths)} folder path(s)."
    )
    return sorted_paths
