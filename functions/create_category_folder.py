"""Create category folders inside the destination root."""

from pathlib import Path



def create_category_folder(destination_root: str, category_name: str) -> str:
    """Create a category folder and return its absolute path."""
    destination_root_path = Path(destination_root)
    if not destination_root_path.is_dir():
        raise NotADirectoryError(
            f"Destination root does not exist: {destination_root_path}"
        )

    normalized_category_name = category_name.strip()
    if not normalized_category_name:
        raise ValueError("Category name cannot be empty.")

    category_path = (destination_root_path / normalized_category_name).resolve()
    category_path.mkdir(parents=True, exist_ok=True)
    return str(category_path)
