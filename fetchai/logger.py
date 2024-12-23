import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
logger: logging.Logger = logging.getLogger("fetchai")
