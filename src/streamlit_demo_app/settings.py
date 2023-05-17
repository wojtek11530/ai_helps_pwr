"""The file with paths to folders used by streamlit app."""

from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()
APP_DIR = Path(__file__).parent.resolve()
CONFIG_DIR = PROJECT_DIR / "config"
