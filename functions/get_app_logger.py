"""Get the shared AppLogger instance."""

from classes.AppLogger import AppLogger

_APP_LOGGER: AppLogger | None = None


def get_app_logger() -> AppLogger:
    """Get the singleton AppLogger for the current process."""
    global _APP_LOGGER
    if _APP_LOGGER is None:
        _APP_LOGGER = AppLogger()
    return _APP_LOGGER
