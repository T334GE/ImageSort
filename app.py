"""Application entry point for the ImageSort desktop app."""

import sys

from PySide6.QtWidgets import QApplication

from classes.MainWindow import MainWindow
from functions.get_app_logger import get_app_logger


def main() -> None:
    """Run the Qt application."""
    logger = get_app_logger()
    logger.log_info("ImageSort app run started.")

    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        exit_code = app.exec()
    except Exception:
        logger.log_exception("Unhandled exception while running ImageSort.")
        raise

    logger.log_info(f"ImageSort app run ended with exit code {exit_code}.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
