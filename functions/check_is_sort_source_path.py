"""Check whether a dropped path is a supported sort source."""

from pathlib import Path

from functions.get_app_logger import get_app_logger
from functions.check_is_image_file import check_is_image_file


def check_is_sort_source_path(source_path: str | Path) -> bool:
    """Return True for folders and supported image files."""
    logger = get_app_logger()
    path = Path(source_path)
    is_valid_source_path = path.is_dir() or check_is_image_file(path)
    logger.log_info(
        f"Checked sort source path '{path}': {is_valid_source_path}."
    )
    return is_valid_source_path
