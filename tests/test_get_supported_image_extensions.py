"""Tests for get_supported_image_extensions."""

from functions.get_supported_image_extensions import get_supported_image_extensions


def test_get_supported_image_extensions_returns_common_extensions() -> None:
    """It should include common image extensions and avoid duplicates."""
    extensions = get_supported_image_extensions()
    assert ".jpg" in extensions
    assert ".png" in extensions
    assert len(extensions) == len(set(extensions))
