"""Resolve a non-conflicting target file path."""

from pathlib import Path

from functions.get_app_logger import get_app_logger



def get_available_file_path(directory_path: str | Path, file_name: str) -> Path:
    """Get a non-conflicting file path inside directory_path for file_name."""
    logger = get_app_logger()
    directory = Path(directory_path)
    if not directory.is_dir():
        logger.log_warning(f"Directory does not exist for path resolution: {directory}")
        raise NotADirectoryError(f"Directory does not exist: {directory}")

    candidate = directory / file_name
    if not candidate.exists():
        logger.log_info(f"Resolved available file path: {candidate}")
        return candidate

    stem = Path(file_name).stem
    suffix = Path(file_name).suffix
    index = 1

    while True:
        candidate = directory / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            logger.log_info(f"Resolved available file path with suffix: {candidate}")
            return candidate
        index += 1
