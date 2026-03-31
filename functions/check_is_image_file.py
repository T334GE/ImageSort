"""Check if a path points to a supported image file."""

from pathlib import Path

from functions.get_app_logger import get_app_logger
from functions.get_supported_image_extensions import get_supported_image_extensions


def check_is_image_file(file_path: str | Path) -> bool:
    """Check whether file_path points to a supported image file."""
    logger = get_app_logger()
    path = Path(file_path)
    is_image_file = path.is_file() and path.suffix.lower() in get_supported_image_extensions()
    logger.log_info(
        f"Checked image file support for path '{path}': {is_image_file}."
    )
    return is_image_file
