import logging
import logging.config
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv(".investd")

path_logging_conf = Path(__file__).parent.parent / "logging.yaml"
if path_logging_conf.exists():
    with path_logging_conf.open("r") as conf_yaml:
        log_conf = yaml.safe_load(conf_yaml)
        logging.config.dictConfig(log_conf)
