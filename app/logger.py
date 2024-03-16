import logging
import sys

from app.config import settings

logger = logging.getLogger("referrals")
stream_handler = logging.StreamHandler(stream=sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s: %(name)s [%(levelname)s] %(message)s"
)
file_handler = logging.FileHandler(
    filename="referrals.log", mode="a", encoding="utf-8"
)
stream_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(settings.LOG_LEVEL)
