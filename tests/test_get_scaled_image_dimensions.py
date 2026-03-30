"""Tests for get_scaled_image_dimensions."""

import pytest

from functions.get_scaled_image_dimensions import get_scaled_image_dimensions


def test_get_scaled_image_dimensions_preserves_aspect_ratio() -> None:
    """It should fit image dimensions inside target bounds with same aspect ratio."""
    assert get_scaled_image_dimensions(4000, 2000, 1000, 1000) == (1000, 500)
    assert get_scaled_image_dimensions(2000, 4000, 1000, 1000) == (500, 1000)


def test_get_scaled_image_dimensions_raises_for_invalid_input() -> None:
    """It should fail when image or target dimensions are not positive."""
    with pytest.raises(ValueError):
        get_scaled_image_dimensions(0, 100, 100, 100)

    with pytest.raises(ValueError):
        get_scaled_image_dimensions(100, 100, 0, 100)
