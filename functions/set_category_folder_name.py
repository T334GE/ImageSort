"""Rename a category folder."""

from pathlib import Path

from functions.get_app_logger import get_app_logger


def set_category_folder_name(category_path: str, category_name: str) -> str:
    """Rename category_path to category_name and return the new absolute path."""
    logger = get_app_logger()
    category_folder = Path(category_path)
    if not category_folder.is_dir():
        logger.log_warning(f"Category folder does not exist for rename: {category_folder}")
        raise NotADirectoryError(f"Category folder does not exist: {category_folder}")

    normalized_category_name = category_name.strip()
    if not normalized_category_name:
        logger.log_warning("Category rename failed because category name is empty.")
        raise ValueError("Category name cannot be empty.")

    if Path(normalized_category_name).name != normalized_category_name:
        logger.log_warning(
            f"Category rename failed because name is not a single folder name: {category_name}"
        )
        raise ValueError("Category name must be a single folder name.")

    source_path = category_folder.resolve()
    target_path = (source_path.parent / normalized_category_name).resolve()

    if target_path == source_path:
        logger.log_info(f"Category rename skipped because source and target are identical: {source_path}")
        return str(source_path)

    if target_path.exists():
        logger.log_warning(f"Category rename target already exists: {target_path}")
        raise FileExistsError(f"Category folder already exists: {target_path}")

    try:
        renamed_path = source_path.rename(target_path).resolve()
    except Exception:
        logger.log_exception(
            f"Failed renaming category folder '{source_path}' to '{target_path}'."
        )
        raise

    logger.log_info(f"Renamed category folder from '{source_path}' to '{renamed_path}'.")
    return str(renamed_path)
