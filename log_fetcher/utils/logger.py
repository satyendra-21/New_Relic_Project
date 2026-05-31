import logging
import os


os.makedirs(
    "log_fetcher_logs",
    exist_ok=True
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            "log_fetcher_logs/fetcher.log"
        ),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger(
    "log_fetcher"
)