import os
from pathlib import Path

from loguru import logger

LOG_PATH = Path(__file__).parents[4] / "logs" / f"{os.getenv('SERVICE_NAME', 'common')}.log"

logger.add(LOG_PATH, rotation="500 MB", serialize=True)
