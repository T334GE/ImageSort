"""Main Qt window for the ImageSort application."""

from pathlib import Path
from typing import Iterable

from PySide6.QtCore import QEvent, QPoint, QSize, Qt, QItemSelectionModel
from PySide6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
    QIcon,
    QKeyEvent,
    QPixmap,
    QResizeEvent,
)
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QListView,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from functions.check_is_sort_source_path import check_is_sort_source_path
from functions.copy_images_to_category import copy_images_to_category
from functions.create_category_folder import create_category_folder
from functions.get_category_paths_from_destination_root import (
    get_category_paths_from_destination_root,
)
from functions.get_image_paths_from_source_paths import get_image_paths_from_source_paths
from functions.get_scaled_image_dimensions import get_scaled_image_dimensions
from functions.move_images_to_category import move_images_to_category
from functions.remove_image_files import remove_image_files
from functions.set_category_folder_name import set_category_folder_name


class MainWindow(QMainWindow):
    """Main window for drag-and-drop image sorting."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ImageSort")
        self.resize(980, 680)
        self.setAcceptDrops(True)

        self._destination_root: str = ""
        self._source_paths: set[str] = set()
        self._loaded_images: set[str] = set()
        self._category_paths: set[str] = set()
        self._preview_image_path: str = ""
        self._thumbnail_size = QSize(120, 120)

        self.create_layout()

    def create_layout(self) -> None:
        """Create and wire the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        instruction_label = QLabel(
            "Drop folders or image files into this window. "
            "Create categories and move selected images into them."
        )
        instruction_label.setWordWrap(True)
        main_layout.addWidget(instruction_label)

        destination_layout = QHBoxLayout()
        destination_label = QLabel("Sort destination:")
        self.destination_input = QLineEdit()
        self.destination_input.setReadOnly(True)
        self.destination_input.setPlaceholderText("Select where category folders will be created")

        self.choose_destination_button = QPushButton("Choose folder")
        self.choose_destination_button.clicked.connect(self.show_destination_picker)

        destination_layout.addWidget(destination_label)
        destination_layout.addWidget(self.destination_input)
        destination_layout.addWidget(self.choose_destination_button)
        main_layout.addLayout(destination_layout)

        self.images_preview_splitter = QSplitter(Qt.Vertical)
        self.images_preview_splitter.setChildrenCollapsible(False)

        images_panel = QWidget()
        images_panel_layout = QVBoxLayout(images_panel)
        images_panel_layout.setContentsMargins(0, 0, 0, 0)
        images_panel_layout.addWidget(QLabel("Loaded images (multi-select supported):"))

        self.images_list = QListWidget()
        self.images_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.images_list.setMinimumHeight(80)
        self.images_list.setFocusPolicy(Qt.StrongFocus)
        self.images_list.installEventFilter(self)
        self.images_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.images_list.customContextMenuRequested.connect(
            self.show_loaded_images_context_menu
        )
        self.configure_images_list_as_icon_view()
        self.images_list.itemSelectionChanged.connect(self.show_selected_image_preview)
        images_panel_layout.addWidget(self.images_list)

        preview_panel = QWidget()
        preview_panel_layout = QVBoxLayout(preview_panel)
        preview_panel_layout.setContentsMargins(0, 0, 0, 0)
        preview_panel_layout.addWidget(QLabel("Selected image preview:"))

        self.image_preview_label = QLabel("Select an image to preview.")
        self.image_preview_label.setAlignment(Qt.AlignCenter)
        self.image_preview_label.setMinimumHeight(80)
        self.image_preview_label.setStyleSheet("QLabel { border: 1px solid #999; }")
        preview_panel_layout.addWidget(self.image_preview_label, 1)

        self.images_preview_splitter.addWidget(images_panel)
        self.images_preview_splitter.addWidget(preview_panel)
        self.images_preview_splitter.setSizes([380, 280])
        self.images_preview_splitter.splitterMoved.connect(
            self.show_selected_image_preview_on_splitter_move
        )
        main_layout.addWidget(self.images_preview_splitter, 1)

        category_input_layout = QHBoxLayout()
        self.category_name_input = QLineEdit()
        self.category_name_input.setPlaceholderText("Category name")

        self.create_category_button = QPushButton("Create category")
        self.create_category_button.clicked.connect(self.create_category_from_input)

        category_input_layout.addWidget(self.category_name_input)
        category_input_layout.addWidget(self.create_category_button)
        main_layout.addLayout(category_input_layout)

        main_layout.addWidget(QLabel("Categories:"))
        self.categories_list = QListWidget()
        self.categories_list.setSelectionMode(QListWidget.SingleSelection)
        self.categories_list.setMinimumHeight(80)
        self.categories_list.setMaximumHeight(120)
        self.categories_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.categories_list.customContextMenuRequested.connect(
            self.show_category_context_menu
        )
        main_layout.addWidget(self.categories_list)

        sort_mode_layout = QHBoxLayout()
        self.remove_original_checkbox = QCheckBox("Remove original (move)")
        self.copy_image_checkbox = QCheckBox("Copy image (keep original)")

        self.sort_mode_group = QButtonGroup(self)
        self.sort_mode_group.setExclusive(True)
        self.sort_mode_group.addButton(self.remove_original_checkbox)
        self.sort_mode_group.addButton(self.copy_image_checkbox)
        self.remove_original_checkbox.setChecked(True)

        sort_mode_layout.addWidget(self.remove_original_checkbox)
        sort_mode_layout.addWidget(self.copy_image_checkbox)
        main_layout.addLayout(sort_mode_layout)

        self.move_images_button = QPushButton(
            "Sort selected images to selected category"
        )
        self.move_images_button.clicked.connect(self.move_selected_images_to_category)
        main_layout.addWidget(self.move_images_button)

    def configure_images_list_as_icon_view(self) -> None:
        """Display loaded images in icon mode with thumbnail cells."""
        self.images_list.setViewMode(QListView.IconMode)
        self.images_list.setMovement(QListView.Static)
        self.images_list.setResizeMode(QListView.Adjust)
        self.images_list.setIconSize(self._thumbnail_size)
        self.images_list.setGridSize(
            QSize(
                self._thumbnail_size.width() + 56,
                self._thumbnail_size.height() + 30,
            )
        )
        self.images_list.setSpacing(8)
        self.images_list.setWordWrap(True)

    def show_destination_picker(self) -> None:
        """Show a dialog to select the destination root folder."""
        destination_root = QFileDialog.getExistingDirectory(
            self,
            "Select sort destination folder",
        )
        if not destination_root:
            return

        self.set_destination_root(str(Path(destination_root).resolve()))

    def set_destination_root(self, destination_root: str) -> None:
        """Set destination root and load existing categories from it."""
        self._destination_root = destination_root
        self.destination_input.setText(destination_root)

        category_paths = get_category_paths_from_destination_root(destination_root)
        self.set_category_paths(category_paths)

    def set_category_paths(self, category_paths: Iterable[str]) -> None:
        """Replace the category list with category_paths."""
        self.categories_list.clear()
        self._category_paths.clear()

        for category_path in category_paths:
            category_item = QListWidgetItem(Path(category_path).name)
            category_item.setData(Qt.UserRole, category_path)
            category_item.setToolTip(category_path)
            self.categories_list.addItem(category_item)
            self._category_paths.add(category_path)

    def create_category_from_input(self) -> None:
        """Create a category from the text input."""
        if not self._destination_root:
            self.show_warning_message("Choose a sort destination first.")
            return

        category_name = self.category_name_input.text().strip()
        if not category_name:
            self.show_warning_message("Enter a category name.")
            return

        category_path = create_category_folder(self._destination_root, category_name)
        if category_path in self._category_paths:
            self.show_warning_message(
                f"Category '{category_name}' already exists in the list.",
                category_path,
            )
            self.category_name_input.clear()
            return

        category_item = QListWidgetItem(category_name)
        category_item.setData(Qt.UserRole, category_path)
        category_item.setToolTip(category_path)
        self.categories_list.addItem(category_item)
        self._category_paths.add(category_path)
        self.category_name_input.clear()

    def show_category_context_menu(self, position: QPoint) -> None:
        """Show available category actions for the clicked item."""
        category_item = self.categories_list.itemAt(position)
        if category_item is None:
            return

        self.categories_list.setCurrentItem(category_item)

        category_menu = QMenu(self)
        rename_category_action = category_menu.addAction("Rename category")
        selected_action = category_menu.exec(
            self.categories_list.viewport().mapToGlobal(position)
        )
        if selected_action != rename_category_action:
            return

        self.show_rename_category_dialog(category_item)

    def show_loaded_images_context_menu(self, position: QPoint) -> None:
        """Show available actions for the clicked loaded-image item."""
        image_item = self.images_list.itemAt(position)
        if image_item is None:
            return

        selected_items = self.images_list.selectedItems()
        target_items = selected_items if image_item in selected_items else [image_item]
        if image_item not in selected_items:
            self.images_list.setCurrentItem(image_item)

        loaded_images_menu = QMenu(self)
        remove_from_listing_action = loaded_images_menu.addAction("Remove from listing")
        remove_from_disk_action = loaded_images_menu.addAction("Remove from disk")
        selected_action = loaded_images_menu.exec(
            self.images_list.viewport().mapToGlobal(position)
        )

        if selected_action == remove_from_listing_action:
            self.remove_image_items_from_listing(target_items)
            return

        if selected_action != remove_from_disk_action:
            return

        self.remove_image_items_from_disk(target_items)

    def remove_image_items_from_listing(
        self,
        image_items: Iterable[QListWidgetItem],
    ) -> None:
        """Remove image items from the loaded-images list without deleting files."""
        for image_item in list(image_items):
            row = self.images_list.row(image_item)
            if row < 0:
                continue

            image_path = str(image_item.data(Qt.UserRole))
            self._loaded_images.discard(image_path)
            self.images_list.takeItem(row)

        self.show_selected_image_preview()

    def remove_image_items_from_disk(
        self,
        image_items: Iterable[QListWidgetItem],
    ) -> None:
        """Delete image files from disk and remove them from the loaded-images list."""
        target_items = list(image_items)
        image_paths = [str(item.data(Qt.UserRole)) for item in target_items]
        if not image_paths:
            return

        path_summary = self.get_path_list_summary(image_paths)
        confirmed = self.show_confirmation_message(
            f"Delete {len(image_paths)} image(s) from disk? This cannot be undone.",
            path_summary,
        )
        if not confirmed:
            return

        remove_image_files(image_paths)
        self.remove_image_items_from_listing(target_items)

        self.show_information_message(
            f"Removed {len(image_paths)} image(s) from disk.",
            path_summary,
        )

    def handle_images_list_key_press(self, event: QKeyEvent) -> bool:
        """Handle keyboard shortcuts while the loaded-images list has focus."""
        key = event.key()
        modifiers = event.modifiers()

        if key == Qt.Key_Delete:
            if modifiers == Qt.ShiftModifier:
                self.remove_selected_images_from_disk()
                return True

            if modifiers == Qt.NoModifier:
                self.remove_selected_images_from_listing()
                return True

            return False

        if modifiers != Qt.NoModifier:
            return False

        if key in (Qt.Key_Up, Qt.Key_Left):
            self.set_loaded_images_current_item_by_offset(-1)
            return True

        if key in (Qt.Key_Down, Qt.Key_Right):
            self.set_loaded_images_current_item_by_offset(1)
            return True

        return False

    def set_loaded_images_current_item_by_offset(self, row_offset: int) -> None:
        """Move loaded-image selection by row_offset."""
        item_count = self.images_list.count()
        if item_count == 0:
            return

        current_row = self.images_list.currentRow()
        if current_row < 0:
            target_row = 0 if row_offset >= 0 else item_count - 1
        else:
            target_row = max(0, min(item_count - 1, current_row + row_offset))

        self.images_list.setCurrentRow(
            target_row,
            QItemSelectionModel.ClearAndSelect,
        )

        target_item = self.images_list.item(target_row)
        if target_item is not None:
            self.images_list.scrollToItem(target_item)

    def remove_selected_images_from_listing(self) -> None:
        """Remove selected loaded-image items from the listing only."""
        selected_items = self.images_list.selectedItems()
        if not selected_items:
            return

        self.remove_image_items_from_listing(selected_items)

    def remove_selected_images_from_disk(self) -> None:
        """Remove selected loaded-image items from disk."""
        selected_items = self.images_list.selectedItems()
        if not selected_items:
            return

        self.remove_image_items_from_disk(selected_items)

    def show_rename_category_dialog(self, category_item: QListWidgetItem) -> None:
        """Prompt for a new category name and apply the rename."""
        current_category_name = category_item.text()
        category_name, accepted = QInputDialog.getText(
            self,
            "Rename category",
            "New category name:",
            text=current_category_name,
        )
        if not accepted:
            return

        normalized_category_name = category_name.strip()
        if not normalized_category_name:
            self.show_warning_message(
                "Category name cannot be empty.",
                f"Current category: {current_category_name}",
            )
            return

        self.set_category_item_name(category_item, normalized_category_name)

    def set_category_item_name(
        self,
        category_item: QListWidgetItem,
        category_name: str,
    ) -> None:
        """Rename a category folder and update the selected list item metadata."""
        source_category_path = Path(str(category_item.data(Qt.UserRole))).resolve()
        target_category_path = (source_category_path.parent / category_name).resolve()

        if target_category_path != source_category_path:
            if str(target_category_path) in self._category_paths:
                self.show_warning_message(
                    f"Category '{category_name}' already exists in the list.",
                    str(target_category_path),
                )
                return

        renamed_category_path = set_category_folder_name(
            str(source_category_path),
            category_name,
        )

        self._category_paths.discard(str(source_category_path))
        self._category_paths.add(renamed_category_path)

        category_item.setText(Path(renamed_category_path).name)
        category_item.setData(Qt.UserRole, renamed_category_path)
        category_item.setToolTip(renamed_category_path)

    def move_selected_images_to_category(self) -> None:
        """Move selected images to the selected category folder."""
        category_item = self.categories_list.currentItem()
        if category_item is None:
            if self._destination_root:
                self.show_warning_message(
                    "Select a category first.",
                    f"Destination folder: {self._destination_root}",
                )
            else:
                self.show_warning_message("Select a category first.")
            return

        selected_items = self.images_list.selectedItems()
        if not selected_items:
            self.show_warning_message("Select one or more images first.")
            return

        image_paths = self.get_selected_image_paths()
        category_path = str(category_item.data(Qt.UserRole))

        if self.copy_image_checkbox.isChecked():
            copy_images_to_category(image_paths, category_path)
            self.show_information_message(
                f"Copied {len(image_paths)} image(s) to category '{category_item.text()}'.",
                category_path,
            )
            return

        move_images_to_category(image_paths, category_path)
        self.remove_image_items_from_listing(selected_items)

        self.show_information_message(
            f"Moved {len(image_paths)} image(s) to category '{category_item.text()}'.",
            category_path,
        )

    def get_selected_image_paths(self) -> list[str]:
        """Get full file paths from the selected image rows."""
        selected_items = self.images_list.selectedItems()
        return [str(item.data(Qt.UserRole)) for item in selected_items]

    def create_image_thumbnail_icon(self, image_path: str) -> QIcon:
        """Create a scaled thumbnail icon for image_path."""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return QIcon()

        scaled_pixmap = pixmap.scaled(
            self._thumbnail_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        return QIcon(scaled_pixmap)

    def show_selected_image_preview(self) -> None:
        """Display a preview of the first selected image."""
        selected_items = self.images_list.selectedItems()
        if not selected_items:
            self.clear_selected_image_preview()
            return

        selected_image_path = str(selected_items[0].data(Qt.UserRole))
        pixmap = QPixmap(selected_image_path)
        if pixmap.isNull():
            self.clear_selected_image_preview("Unable to preview selected image.")
            return

        target_width = max(1, self.image_preview_label.width() - 12)
        target_height = max(1, self.image_preview_label.height() - 12)
        scaled_width, scaled_height = get_scaled_image_dimensions(
            pixmap.width(),
            pixmap.height(),
            target_width,
            target_height,
        )
        scaled_pixmap = pixmap.scaled(
            scaled_width,
            scaled_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self._preview_image_path = selected_image_path
        self.image_preview_label.setPixmap(scaled_pixmap)
        self.image_preview_label.setText("")
        self.image_preview_label.setToolTip(selected_image_path)

    def clear_selected_image_preview(
        self,
        message: str = "Select an image to preview.",
    ) -> None:
        """Clear the preview area and show a fallback message."""
        self._preview_image_path = ""
        self.image_preview_label.clear()
        self.image_preview_label.setText(message)
        self.image_preview_label.setToolTip("")

    def set_source_paths(self, source_paths: Iterable[str]) -> None:
        """Add dropped source paths and load their image files."""
        new_source_paths = [
            source_path
            for source_path in source_paths
            if source_path not in self._source_paths
        ]

        if not new_source_paths:
            return

        for source_path in new_source_paths:
            self._source_paths.add(source_path)

        image_paths = get_image_paths_from_source_paths(new_source_paths)
        self.set_loaded_images(image_paths)

    def set_loaded_images(self, image_paths: Iterable[str]) -> None:
        """Add image paths to the image list without duplicates."""
        for image_path in image_paths:
            if image_path in self._loaded_images:
                continue

            image_item = QListWidgetItem(Path(image_path).name)
            image_item.setIcon(self.create_image_thumbnail_icon(image_path))
            image_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            image_item.setData(Qt.UserRole, image_path)
            image_item.setToolTip(image_path)

            self.images_list.addItem(image_item)
            self._loaded_images.add(image_path)

    def get_dropped_source_paths(
        self,
        event: QDropEvent | QDragEnterEvent,
    ) -> list[str]:
        """Extract folder and image-file source paths from drop URLs."""
        source_paths: list[str] = []

        if not event.mimeData().hasUrls():
            return source_paths

        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if not local_path:
                continue

            resolved_path = str(Path(local_path).resolve())
            if check_is_sort_source_path(resolved_path):
                source_paths.append(resolved_path)

        return source_paths

    def eventFilter(self, watched: object, event: QEvent) -> bool:
        """Handle loaded-images keyboard shortcuts via event filtering."""
        if watched == self.images_list and event.type() == QEvent.KeyPress:
            if self.handle_images_list_key_press(event):
                return True

        return super().eventFilter(watched, event)

    def get_path_list_summary(
        self,
        paths: Iterable[str],
        maximum_lines: int = 3,
    ) -> str:
        """Get a compact multiline summary for one or more file paths."""
        resolved_paths = [str(Path(path).resolve()) for path in paths]
        if not resolved_paths:
            return ""

        displayed_paths = resolved_paths[:maximum_lines]
        remaining_count = len(resolved_paths) - len(displayed_paths)
        if remaining_count > 0:
            displayed_paths.append(f"... and {remaining_count} more")

        return "\n".join(displayed_paths)

    def show_information_message(
        self,
        message: str,
        details: str = "",
    ) -> None:
        """Show an information dialog with optional details."""
        full_message = message if not details else f"{message}\n{details}"
        QMessageBox.information(self, "ImageSort", full_message)

    def show_confirmation_message(
        self,
        message: str,
        details: str = "",
    ) -> bool:
        """Show a yes/no confirmation dialog and return True on Yes."""
        full_message = message if not details else f"{message}\n{details}"
        confirmed = QMessageBox.question(
            self,
            "ImageSort",
            full_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return confirmed == QMessageBox.Yes

    def show_warning_message(
        self,
        message: str,
        details: str = "",
    ) -> None:
        """Show a warning dialog with optional details."""
        full_message = message if not details else f"{message}\n{details}"
        QMessageBox.warning(self, "ImageSort", full_message)

    def show_selected_image_preview_on_splitter_move(
        self,
        _position: int,
        _index: int,
    ) -> None:
        """Refresh preview scaling when the splitter handle is moved."""
        if not self._preview_image_path:
            return

        self.show_selected_image_preview()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Keep the selected-image preview scaled when the window is resized."""
        super().resizeEvent(event)
        if not self._preview_image_path:
            return

        self.show_selected_image_preview()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Accept drag events containing folders or supported image files."""
        dropped_source_paths = self.get_dropped_source_paths(event)
        if dropped_source_paths:
            event.acceptProposedAction()
            return

        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle dropped folders/files by loading supported image files."""
        dropped_source_paths = self.get_dropped_source_paths(event)
        if not dropped_source_paths:
            self.show_warning_message("Drop one or more folders or image files.")
            event.ignore()
            return

        self.set_source_paths(dropped_source_paths)
        event.acceptProposedAction()
