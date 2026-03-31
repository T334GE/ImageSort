"""Create category folders inside the destination root."""

from pathlib import Path

from functions.get_app_logger import get_app_logger



def create_category_folder(destination_root: str, category_name: str) -> str:
    """Create a category folder and return its absolute path."""
    logger = get_app_logger()
    destination_root_path = Path(destination_root)
    if not destination_root_path.is_dir():
        logger.log_warning(
            f"Destination root does not exist for category creation: {destination_root_path}"
        )
        raise NotADirectoryError(
            f"Destination root does not exist: {destination_root_path}"
        )

    normalized_category_name = category_name.strip()
    if not normalized_category_name:
        logger.log_warning("Category creation failed because category name is empty.")
        raise ValueError("Category name cannot be empty.")

    category_path = (destination_root_path / normalized_category_name).resolve()
    try:
        category_path.mkdir(parents=True, exist_ok=True)
    except Exception:
        logger.log_exception(f"Failed creating category folder: {category_path}")
        raise

    logger.log_info(f"Category folder ready: {category_path}")
    return str(category_path)
