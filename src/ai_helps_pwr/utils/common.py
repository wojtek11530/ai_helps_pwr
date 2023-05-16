"""Common methods."""
import importlib
import json
from pathlib import Path
from typing import Dict, List


def load_model_from_config(cfg: dict):
    """Create an object based on the specified module path and kwargs."""
    module_name, class_name = cfg["module"].rsplit(".", maxsplit=1)

    class_object = getattr(
        importlib.import_module(module_name),
        class_name,
    )

    return class_object(**cfg["kwargs"])


def load_json(path_to_json: Path) -> List[Dict[str, str]]:
    """Load json file."""
    f = open(path_to_json)
    data = json.load(f)
    f.close()
    return data
