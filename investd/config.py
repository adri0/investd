"""
    Configuration

    Config variables are obtained from environment variables and converted
    to their object type.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any

from .model import Currency

log = logging.getLogger(__name__)

SOURCE_BASE_PATH = Path(os.getenv("SOURCE_BASE_PATH", "data/source"))
PERSIST_PATH = Path(os.getenv("PERSIST_PATH", "data/persist"))
REPORTS_PATH = Path(os.getenv("REPORTS_PATH", "data/reports"))
REF_CURRENCY = Currency(os.getenv("REF_CURRENCY", "USD"))


def get_config_variables() -> dict[str, Any]:
    """Get all variables in current module that are uppercase"""
    return {
        env_var: getattr(sys.modules[__name__], env_var)
        for env_var in dir(sys.modules[__name__])
        if env_var.isupper()
    }


log.info(
    " - ".join([f"{name}: {value}" for name, value in get_config_variables().items()])
)

for conf_path in (SOURCE_BASE_PATH, PERSIST_PATH, REPORTS_PATH):
    if not conf_path.exists():
        os.makedirs(conf_path)
