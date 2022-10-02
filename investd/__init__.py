import logging
import logging.config

import yaml

with open("logging.yaml", "r") as log_conf_file:
    log_conf = yaml.safe_load(log_conf_file)
    logging.config.dictConfig(log_conf)
