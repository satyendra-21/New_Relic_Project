import logging
import os
from crud_app.utils.newrelic_handler import NewRelicLogHandler

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("support-ticket-service")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers on reload
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    
    file_handler = logging.FileHandler("logs/application.log")
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    nr_handler = NewRelicLogHandler(batch_size=1, flush_interval=1)
    nr_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.addHandler(nr_handler)
    
    # Prevent propagation to Uvicorn's root logger
    logger.propagate = False