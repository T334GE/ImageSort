"""Check whether a dropped path is a supported sort source."""

from pathlib import Path

from functions.check_is_image_file import check_is_image_file


def check_is_sort_source_path(source_path: str | Path) -> bool:
    """Return True for folders and supported image files."""
    path = Path(source_path)
    return path.is_dir() or check_is_image_file(path)
