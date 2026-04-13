"""Run a callable on a worker thread and emit its result."""

from collections.abc import Callable

from PySide6.QtCore import QObject, Signal, Slot


class TaskWorker(QObject):
    """Execute a task callable in a background thread."""

    completed = Signal(object)
    failed = Signal(object)

    def __init__(self, task: Callable[[], object]) -> None:
        super().__init__()
        self._task = task

    @Slot()
    def run(self) -> None:
        """Execute the configured task and emit completion or failure."""
        try:
            result = self._task()
        except (OSError, RuntimeError, ValueError) as error:
            self.failed.emit(error)
            return

        self.completed.emit(result)
