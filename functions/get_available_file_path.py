"""Resolve a non-conflicting target file path."""

from pathlib import Path



def get_available_file_path(directory_path: str | Path, file_name: str) -> Path:
    """Get a non-conflicting file path inside directory_path for file_name."""
    directory = Path(directory_path)
    if not directory.is_dir():
        raise NotADirectoryError(f"Directory does not exist: {directory}")

    candidate = directory / file_name
    if not candidate.exists():
        return candidate

    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    index = 1

    while True:
        candidate = directory / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1
