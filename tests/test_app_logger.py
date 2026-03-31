"""Tests for AppLogger."""

from pathlib import Path

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
