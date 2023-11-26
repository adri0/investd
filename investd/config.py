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

from investd.common import Currency

log = logging.getLogger(__name__)

INVESTD_DATA = Path(os.getenv("INVESTD_DATA", "investd_data"))
INVESTD_SOURCES = Path(os.getenv("INVESTD_SOURCES", INVESTD_DATA / "sources"))
INVESTD_PERSIST = Path(os.getenv("INVESTD_PERSIST", INVESTD_DATA / "persist"))
INVESTD_REPORTS = Path(os.getenv("INVESTD_REPORTS", INVESTD_DATA / "reports"))
INVESTD_REF_CURRENCY = Currency(os.getenv("INVESTD_REF_CURRENCY", "USD"))


def get_config_variables() -> dict[str, Any]:
    """Get all variables in current module that are uppercase"""
    return {
        env_var: getattr(sys.modules[__name__], env_var)
        for env_var in dir(sys.modules[__name__])
        if env_var.isupper()
    }


def init_dirs() -> None:
    """
    Check if data dirs exist, create them otherwise.
    """
    config_vars = get_config_variables().items()
    log.info(", ".join(f"{name}: {value}" for name, value in config_vars))
    if not INVESTD_DATA.exists():
        print(
            f"INVESTD_DATA directory ({INVESTD_DATA}) doesn't exist. "
            "Let me create it for you."
        )
        INVESTD_DATA.mkdir(exist_ok=True, parents=True)
