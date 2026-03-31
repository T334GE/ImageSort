# ImageSort

Desktop app (Python + Qt) for sorting images by category. (Requested by a friend)

<img width="1917" height="1026" alt="image" src="https://github.com/user-attachments/assets/6f7b849f-1ffa-434f-8d90-20463f09d1da" />

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

<img width="551" height="245" alt="image" src="https://github.com/user-attachments/assets/7495333d-73e2-435d-a099-679b925ac3e2" />

<img width="1915" height="1036" alt="image" src="https://github.com/user-attachments/assets/22b042fe-29b8-4b8e-8654-c276015b2c8c" />

## Dependencies

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
