"""Module with email categories loaded from json file."""
from ai_helps_pwr.settings import DATA_DIR
from ai_helps_pwr.utils.common import load_json

categories_list = load_json(DATA_DIR / "email_categories.json")

CATEGORIES = {c["name"]: c for c in categories_list}
