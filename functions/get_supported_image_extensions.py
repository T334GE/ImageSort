"""Return supported image extensions."""


def get_supported_image_extensions() -> tuple[str, ...]:
    """Get the supported image file extensions."""
    return (
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".gif",
        ".webp",
        ".tif",
        ".tiff",
    )
