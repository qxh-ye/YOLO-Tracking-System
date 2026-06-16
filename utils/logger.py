import logging
import os.path


def get_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    logger = logging.getLogger("tracking")

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            "logs/app.log",
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger