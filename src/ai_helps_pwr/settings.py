"""The file with paths to folders used in the project."""

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_DIR / "data"
STORAGE_DIR = PROJECT_DIR / "storage"
