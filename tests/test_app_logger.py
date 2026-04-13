"""Tests for AppLogger."""

from pathlib import Path

from PySide6.QtCore import QtMsgType

from classes.AppLogger import AppLogger


def test_app_logger_creates_error_log_on_first_error(tmp_path: Path) -> None:
    """It should create error.log only after the first error is logged."""
    logs_directory = tmp_path / "logs"
    logger = AppLogger(logs_directory)

    run_log_path = logs_directory / "run.log"
    error_log_path = logs_directory / "error.log"

    logger.log_info("info-message")

    assert run_log_path.exists()
    assert not error_log_path.exists()

    logger.log_error("error-message")

    assert error_log_path.exists()

    assert "info-message" in run_log_path.read_text(encoding="utf-8")
    assert "error-message" in run_log_path.read_text(encoding="utf-8")
    assert "error-message" in error_log_path.read_text(encoding="utf-8")


def test_app_logger_overwrites_run_log_for_new_run(tmp_path: Path) -> None:
    """It should overwrite run.log when a new logger run is configured."""
    logs_directory = tmp_path / "logs"
    first_run_logger = AppLogger(logs_directory)
    first_run_logger.log_info("first-run-message")

    second_run_logger = AppLogger(logs_directory)
    second_run_logger.log_info("second-run-message")

    run_log_contents = (logs_directory / "run.log").read_text(encoding="utf-8")
    assert "second-run-message" in run_log_contents
    assert "first-run-message" not in run_log_contents


def test_app_logger_notifies_registered_message_listeners(tmp_path: Path) -> None:
    """It should send formatted log messages to registered listeners only while subscribed."""
    logs_directory = tmp_path / "logs"
    logger = AppLogger(logs_directory)
    received_messages: list[str] = []
    listener = received_messages.append

    logger.add_message_listener(listener)
    logger.log_info("listener-info-message")
    logger.remove_message_listener(listener)
    logger.log_warning("listener-warning-message")

    assert len(received_messages) == 1
    assert "INFO" in received_messages[0]
    assert "listener-info-message" in received_messages[0]
    assert "listener-warning-message" not in received_messages[0]


def test_app_logger_routes_qt_messages_to_matching_log_levels(tmp_path: Path) -> None:
    """It should write Qt warnings to run.log and Qt criticals to error.log."""
    logs_directory = tmp_path / "logs"
    logger = AppLogger(logs_directory)

    run_log_path = logs_directory / "run.log"
    error_log_path = logs_directory / "error.log"

    logger.log_qt_message(QtMsgType.QtWarningMsg, "qt-warning-message")

    assert run_log_path.exists()
    assert not error_log_path.exists()
    assert "qt-warning-message" in run_log_path.read_text(encoding="utf-8")

    logger.log_qt_message(QtMsgType.QtCriticalMsg, "qt-critical-message")

    assert error_log_path.exists()
    assert "qt-critical-message" in run_log_path.read_text(encoding="utf-8")
    assert "qt-critical-message" in error_log_path.read_text(encoding="utf-8")
