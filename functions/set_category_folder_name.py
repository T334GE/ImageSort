"""Rename a category folder."""

from pathlib import Path


def set_category_folder_name(category_path: str, category_name: str) -> str:
    """Rename category_path to category_name and return the new absolute path."""
    category_folder = Path(category_path)
    if not category_folder.is_dir():
        raise NotADirectoryError(f"Category folder does not exist: {category_folder}")

    normalized_category_name = category_name.strip()
    if not normalized_category_name:
        raise ValueError("Category name cannot be empty.")

    if Path(normalized_category_name).name != normalized_category_name:
        raise ValueError("Category name must be a single folder name.")

    source_path = category_folder.resolve()
    target_path = (source_path.parent / normalized_category_name).resolve()

    if target_path == source_path:
        return str(source_path)

    if target_path.exists():
        raise FileExistsError(f"Category folder already exists: {target_path}")

    renamed_path = source_path.rename(target_path).resolve()
    return str(renamed_path)
