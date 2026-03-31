"""Get existing category folder paths from a destination root."""

from pathlib import Path

from functions.get_app_logger import get_app_logger


def get_category_paths_from_destination_root(destination_root: str) -> list[str]:
    """Return immediate child folders of destination_root as absolute paths."""
    logger = get_app_logger()
    destination_root_path = Path(destination_root)
    if not destination_root_path.is_dir():
        logger.log_warning(
            f"Destination root does not exist for category discovery: {destination_root_path}"
        )
        raise NotADirectoryError(
            f"Destination root does not exist: {destination_root_path}"
        )

    category_paths = [
        str(child_path.resolve())
        for child_path in destination_root_path.iterdir()
        if child_path.is_dir()
    ]
    sorted_paths = sorted(category_paths, key=lambda path: Path(path).name.lower())
    logger.log_info(
        f"Discovered {len(sorted_paths)} category folder(s) in '{destination_root_path.resolve()}'."
    )
    return sorted_paths
