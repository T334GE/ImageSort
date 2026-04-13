"""Application logger utilities for ImageSort."""

import logging
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Final

from PySide6.QtCore import QMessageLogContext, QtMsgType, qInstallMessageHandler


class AppLogger:
    """Centralized file logger for ImageSort application events."""

    LOGGER_NAME: Final[str] = "imagesort"
    LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(message)s"

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
        self._message_formatter = logging.Formatter(self.LOG_FORMAT)
        self._message_listeners: list[Callable[[str], None]] = []
        self._previous_qt_message_handler: Callable[[QtMsgType, QMessageLogContext, str], None] | None = None
        self._qt_message_handler_installed = False

        self.configure_handlers()

    @staticmethod
    def get_default_logs_directory() -> Path:
        """Get the default log directory under the project root."""
        project_root = Path(__file__).resolve().parent.parent
        return project_root / "logs"

    def configure_handlers(self) -> None:
        """Configure run and error file handlers."""
        log_format = logging.Formatter(self.LOG_FORMAT)

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

    def add_message_listener(self, listener: Callable[[str], None]) -> None:
        """Register a listener for formatted log messages."""
        if listener in self._message_listeners:
            return

        self._message_listeners.append(listener)

    def install_qt_message_handler(self) -> None:
        """Install the Qt message handler so framework warnings are logged too."""
        if self._qt_message_handler_installed:
            return

        self._previous_qt_message_handler = qInstallMessageHandler(self.handle_qt_message)
        self._qt_message_handler_installed = True

    def restore_qt_message_handler(self) -> None:
        """Restore the previously installed Qt message handler."""
        if not self._qt_message_handler_installed:
            return

        qInstallMessageHandler(self._previous_qt_message_handler)
        self._previous_qt_message_handler = None
        self._qt_message_handler_installed = False

    def remove_message_listener(self, listener: Callable[[str], None]) -> None:
        """Unregister a previously added message listener."""
        if listener not in self._message_listeners:
            return

        self._message_listeners.remove(listener)

    def notify_message_listeners(
        self,
        level: int,
        message: str,
        exc_info: tuple[type[BaseException], BaseException, object] | None = None,
    ) -> None:
        """Send a formatted log line to all registered listeners."""
        if not self._message_listeners:
            return

        log_record = self._logger.makeRecord(
            self.LOGGER_NAME,
            level,
            fn="",
            lno=0,
            msg=message,
            args=(),
            exc_info=exc_info,
            func=None,
            extra=None,
        )
        formatted_message = self._message_formatter.format(log_record)

        for listener in tuple(self._message_listeners):
            listener(formatted_message)

    def format_qt_message(
        self,
        message: str,
        context: QMessageLogContext | None,
    ) -> str:
        """Format a Qt framework log message with available context details."""
        context_parts: list[str] = []
        if context is not None:
            if context.category:
                context_parts.append(f"category={context.category}")
            if context.file:
                context_parts.append(f"file={context.file}")
            if context.line > 0:
                context_parts.append(f"line={context.line}")
            if context.function:
                context_parts.append(f"function={context.function}")

        if not context_parts:
            return f"Qt message: {message}"

        return f"Qt message: {message} ({', '.join(context_parts)})"

    def log_qt_message(
        self,
        message_type: QtMsgType,
        message: str,
        context: QMessageLogContext | None = None,
    ) -> None:
        """Forward a Qt framework log message into the application logger."""
        formatted_message = self.format_qt_message(message, context)

        if message_type in (QtMsgType.QtDebugMsg, QtMsgType.QtInfoMsg):
            self.log_info(formatted_message)
            return

        if message_type == QtMsgType.QtWarningMsg:
            self.log_warning(formatted_message)
            return

        if message_type in (QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg):
            self.log_error(formatted_message)
            return

        self.log_warning(formatted_message)

    def handle_qt_message(
        self,
        message_type: QtMsgType,
        context: QMessageLogContext,
        message: str,
    ) -> None:
        """Handle Qt framework log messages and pass them into AppLogger."""
        self.log_qt_message(message_type, message, context)

        if self._previous_qt_message_handler is None:
            return

        self._previous_qt_message_handler(message_type, context, message)

    def log_info(self, message: str) -> None:
        """Log an informational message."""
        self._logger.info(message)
        self.notify_message_listeners(logging.INFO, message)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warning(message)
        self.notify_message_listeners(logging.WARNING, message)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)
        self.notify_message_listeners(logging.ERROR, message)

    def log_exception(self, message: str) -> None:
        """Log an exception traceback message."""
        self._logger.exception(message)
        self.notify_message_listeners(logging.ERROR, message, sys.exc_info())
