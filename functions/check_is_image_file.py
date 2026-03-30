"""Check if a path points to a supported image file."""

from pathlib import Path

from functions.get_supported_image_extensions import get_supported_image_extensions


def check_is_image_file(file_path: str | Path) -> bool:
    """Check whether file_path points to a supported image file."""
    path = Path(file_path)
    return path.is_file() and path.suffix.lower() in get_supported_image_extensions()
