"""Remove image files from disk."""

from pathlib import Path
from typing import Iterable


def remove_image_files(image_paths: Iterable[str]) -> list[str]:
    """Delete image_paths from disk and return removed absolute paths."""
    removed_paths: list[str] = []

    for image_path in image_paths:
        source_path = Path(image_path)
        if not source_path.is_file():
            raise FileNotFoundError(f"Image file does not exist: {source_path}")

        source_path.unlink()
        removed_paths.append(str(source_path.resolve()))

    return removed_paths
