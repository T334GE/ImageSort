# ImageSort

Desktop app (Python + Qt) for sorting images by category.

## What it does

- Drag one or more **folders or image files** into the app.
- App loads image files recursively from dropped folders and directly from dropped image files.
- Selecting an image in the list shows a preview in the app.
- Create categories (folders) in the UI.
- Choosing a destination folder auto-loads its existing child folders as categories.
- Choose sort mode with checkboxes: remove original (move) or copy image.
- Only one sort mode checkbox can be selected at a time.
- Right-click a category to rename its folder.
- Move selected images into a selected category folder.

## Tech stack

- Python 3.11+
- PySide6 (Qt for Python)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Test

```bash
pytest -q
```
