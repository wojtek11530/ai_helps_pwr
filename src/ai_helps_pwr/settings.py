"""The file with paths to folders used in the project."""

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()
DATA_DIR = PROJECT_DIR / "data"
STORAGE_DIR = PROJECT_DIR / "storage"
CONFIG_DIR = PROJECT_DIR / "config"

DEFAULT_OPENAI_API_CONFIG = CONFIG_DIR / "config.local"
