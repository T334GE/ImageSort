"""Get existing category folder paths from a destination root."""

from pathlib import Path


def get_category_paths_from_destination_root(destination_root: str) -> list[str]:
    """Return immediate child folders of destination_root as absolute paths."""
    destination_root_path = Path(destination_root)
    if not destination_root_path.is_dir():
        raise NotADirectoryError(
            f"Destination root does not exist: {destination_root_path}"
        )

    category_paths = [
        str(child_path.resolve())
        for child_path in destination_root_path.iterdir()
        if child_path.is_dir()
    ]
    return sorted(category_paths, key=lambda path: Path(path).name.lower())
