"""Remove image files from disk."""

from pathlib import Path
from typing import Iterable

from functions.get_app_logger import get_app_logger


def remove_image_files(image_paths: Iterable[str]) -> list[str]:
    """Delete image_paths from disk and return removed absolute paths."""
    logger = get_app_logger()
    removed_paths: list[str] = []

    for image_path in image_paths:
        source_path = Path(image_path)
        if not source_path.is_file():
            logger.log_warning(f"Remove-from-disk source file does not exist: {source_path}")
            raise FileNotFoundError(f"Image file does not exist: {source_path}")

        try:
            source_path.unlink()
        except Exception:
            logger.log_exception(f"Failed deleting image file: {source_path}")
            raise

        resolved_path = str(source_path.resolve())
        removed_paths.append(resolved_path)
        logger.log_info(f"Deleted image file: {resolved_path}")

    logger.log_info(f"Deleted {len(removed_paths)} image file(s) from disk.")
    return removed_paths
