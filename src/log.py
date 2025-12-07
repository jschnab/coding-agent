import logging


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_path: str = "log",
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
