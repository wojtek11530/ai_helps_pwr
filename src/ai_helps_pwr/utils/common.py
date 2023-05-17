"""Common methods."""
import configparser
import importlib
import json
from pathlib import Path

from ai_helps_pwr.settings import DEFAULT_OPENAI_API_CONFIG


def load_model_from_config(cfg: dict):
    """Create an object based on the specified module path and kwargs."""
    module_name, class_name = cfg["module"].rsplit(".", maxsplit=1)

    class_object = getattr(
        importlib.import_module(module_name),
        class_name,
    )

    return class_object(**cfg["kwargs"])


def load_json(path_to_json: Path) -> list[dict[str, str]]:
    """Load json file."""
    with open(path_to_json, encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_openai_api_key(
    config_path: Path = Path(DEFAULT_OPENAI_API_CONFIG),
) -> str:
    """Load OpenAI API key from config file."""
    config = configparser.RawConfigParser()
    config.read(config_path)
    gpt_config = dict(config.items("gpt"))
    return gpt_config["apikey"]


def get_email_credentials(
    config_path: Path = Path(DEFAULT_OPENAI_API_CONFIG),
) -> tuple[str, str]:
    """Load email credentials from config file."""
    config = configparser.RawConfigParser()
    config.read(config_path)
    email_config = dict(config.items("email"))
    return email_config["sender"], email_config["password"]
