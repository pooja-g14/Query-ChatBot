import logging
import sys

# Configure standard Python logging format and stream handlers
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Export a configured logger instance
logger = logging.getLogger("Query-ChatBot")
