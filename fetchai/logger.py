import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())


def get_logger(name: str):
    return logging.getLogger(name)
