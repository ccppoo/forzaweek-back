import logging


logger = logging.getLogger(__name__)
log_format = "%(asctime)s [%(levelname)s] %(message)s"
log_date_format = "%Y-%m-%d %I:%M:%S %p"
logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    level=logging.INFO,
    format=log_format,
    datefmt=log_date_format,
)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(message)s", datefmt=log_date_format
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_logger():
    return logger
