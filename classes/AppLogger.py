"""Application logger utilities for ImageSort."""

import logging
from pathlib import Path
from typing import Final


class AppLogger:
    """Centralized file logger for ImageSort application events."""

    LOGGER_NAME: Final[str] = "imagesort"

    def __init__(self, logs_directory: str | Path | None = None) -> None:
        if logs_directory is None:
            self._logs_directory = self.get_default_logs_directory()
        else:
            self._logs_directory = Path(logs_directory).resolve()

        self._logs_directory.mkdir(parents=True, exist_ok=True)

        self._run_log_path = self._logs_directory / "run.log"
        self._error_log_path = self._logs_directory / "error.log"

        self._logger = logging.getLogger(self.LOGGER_NAME)
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        self.configure_handlers()

    @staticmethod
    def get_default_logs_directory() -> Path:
        """Get the default log directory under the project root."""
        project_root = Path(__file__).resolve().parent.parent
        return project_root / "logs"

    def configure_handlers(self) -> None:
        """Configure run and error file handlers."""
        log_format = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        for handler in list(self._logger.handlers):
            self._logger.removeHandler(handler)
            handler.close()

        run_handler = logging.FileHandler(self._run_log_path, mode="w", encoding="utf-8")
        run_handler.setLevel(logging.INFO)
        run_handler.setFormatter(log_format)

        error_handler = logging.FileHandler(
            self._error_log_path,
            mode="a",
            encoding="utf-8",
            delay=True,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(log_format)

        self._logger.addHandler(run_handler)
        self._logger.addHandler(error_handler)

    def log_info(self, message: str) -> None:
        """Log an informational message."""
        self._logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)

    def log_exception(self, message: str) -> None:
        """Log an exception traceback message."""
        self._logger.exception(message)
