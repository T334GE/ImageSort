"""Application entry point for the ImageSort desktop app."""

import sys

from PySide6.QtWidgets import QApplication

from classes.MainWindow import MainWindow


def main() -> None:
    """Run the Qt application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
