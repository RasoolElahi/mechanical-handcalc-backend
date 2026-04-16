
from __future__ import annotations

import importlib
from typing import Any


def load_plugin_module(module_path: str) -> Any:
    module_name = module_path.replace('/', '.') + '.plugin'
    return importlib.import_module(module_name)
