"""Return supported image extensions."""

from functions.get_app_logger import get_app_logger


def get_supported_image_extensions() -> tuple[str, ...]:
    """Get the supported image file extensions."""
    logger = get_app_logger()
    supported_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".webp",
        ".tif",
        ".tiff",
    )
    logger.log_info(
        f"Loaded supported image extensions ({len(supported_extensions)} values)."
    )
    return supported_extensions
