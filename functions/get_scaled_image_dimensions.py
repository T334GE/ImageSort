"""Calculate scaled dimensions for image previews."""

from functions.get_app_logger import get_app_logger


def get_scaled_image_dimensions(
    image_width: int,
    image_height: int,
    target_width: int,
    target_height: int,
) -> tuple[int, int]:
    """Return dimensions that fit target bounds while preserving aspect ratio."""
    logger = get_app_logger()
    if image_width <= 0 or image_height <= 0:
        logger.log_warning(
            f"Invalid source image dimensions: width={image_width}, height={image_height}."
        )
        raise ValueError("Image dimensions must be greater than zero.")

    if target_width <= 0 or target_height <= 0:
        logger.log_warning(
            f"Invalid target dimensions: width={target_width}, height={target_height}."
        )
        raise ValueError("Target dimensions must be greater than zero.")

    width_scale = target_width / image_width
    height_scale = target_height / image_height
    scale = min(width_scale, height_scale)

    scaled_width = max(1, int(image_width * scale))
    scaled_height = max(1, int(image_height * scale))
    logger.log_info(
        "Scaled image dimensions "
        f"from ({image_width}, {image_height}) "
        f"to ({scaled_width}, {scaled_height}) "
        f"within target ({target_width}, {target_height})."
    )
    return scaled_width, scaled_height
