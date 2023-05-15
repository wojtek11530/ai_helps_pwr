"""Common methods."""
import importlib
import json
from pathlib import Path


def load_model_from_config(cfg: dict):
    """Create an object based on the specified module path and kwargs."""
    module_name, class_name = cfg["module"].rsplit(".", maxsplit=1)

    cls = getattr(
        importlib.import_module(module_name),
        class_name,
    )

    return cls(**cfg["kwargs"])


def load_prompt(path_to_json: Path):
    """Load json file."""
    f = open(path_to_json)
    data = json.load(f)
    f.close()
    return data
