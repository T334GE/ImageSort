"""Collect image paths from folders and/or direct image file paths."""

from pathlib import Path
from typing import Iterable

from functions.get_app_logger import get_app_logger
from functions.check_is_image_file import check_is_image_file


def get_image_paths_from_source_paths(source_paths: Iterable[str]) -> list[str]:
    """Resolve image paths from source paths.

    Each source path must be either:
    - a folder (searched recursively)
    - a supported image file
    """
    logger = get_app_logger()
    normalized_source_paths = list(source_paths)
    image_paths: set[str] = set()

    for source_path in normalized_source_paths:
        path = Path(source_path)

        if path.is_dir():
            logger.log_info(f"Scanning dropped folder source: {path.resolve()}")
            for file_path in path.rglob("*"):
                if check_is_image_file(file_path):
                    image_paths.add(str(file_path.resolve()))
            continue

        if check_is_image_file(path):
            logger.log_info(f"Accepted dropped image file source: {path.resolve()}")
            image_paths.add(str(path.resolve()))
            continue

        logger.log_warning(
            f"Rejected unsupported source path (not folder or supported image): {path}"
        )
        raise ValueError(
            f"Source path must be a folder or supported image file: {path}"
        )

    sorted_paths = sorted(image_paths)
    logger.log_info(
        f"Resolved {len(sorted_paths)} image file(s) from {len(normalized_source_paths)} source path(s)."
    )
    return sorted_paths
