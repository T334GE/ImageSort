"""Greyed-out loading overlay that displays live log messages."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPlainTextEdit, QVBoxLayout, QWidget


class LoadingOverlay(QWidget):
    """Display a blocking loading overlay with a live log view."""

    message_logged = Signal(str)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgba(90, 90, 90, 160);")
        self.setFocusPolicy(Qt.StrongFocus)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(48, 48, 48, 48)
        outer_layout.addStretch()

        panel = QFrame(self)
        panel.setStyleSheet(
            "QFrame {"
            "background-color: rgba(28, 28, 28, 230);"
            "border: 1px solid #707070;"
            "border-radius: 10px;"
            "}"
            "QLabel { color: #f2f2f2; border: none; }"
            "QPlainTextEdit {"
            "background-color: #101010;"
            "color: #f2f2f2;"
            "border: 1px solid #5a5a5a;"
            "border-radius: 6px;"
            "}"
        )
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(12)

        self.status_label = QLabel("Working...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        panel_layout.addWidget(self.status_label)

        self.log_messages_view = QPlainTextEdit()
        self.log_messages_view.setReadOnly(True)
        self.log_messages_view.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_messages_view.document().setMaximumBlockCount(200)
        panel_layout.addWidget(self.log_messages_view)

        outer_layout.addWidget(panel)
        outer_layout.addStretch()

        self.message_logged.connect(self.append_log_message)
        self.hide()

    def show_loading(self, status_text: str) -> None:
        """Show the overlay and reset the visible task state."""
        self.status_label.setText(status_text)
        self.log_messages_view.clear()
        self.show()
        self.raise_()
        self.setFocus()

    def hide_loading(self) -> None:
        """Hide the overlay."""
        self.hide()

    def set_status_text(self, status_text: str) -> None:
        """Update the loading status text."""
        self.status_label.setText(status_text)

    def append_log_message(self, message: str) -> None:
        """Append a formatted log line while the overlay is visible."""
        if not self.isVisible():
            return

        self.log_messages_view.appendPlainText(message)
        scrollbar = self.log_messages_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
