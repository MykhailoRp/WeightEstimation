import logging
import sys
from types import FrameType

from loguru import _defaults, logger

from common.service_config import ServiceConfig


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame: FrameType | None
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_logging() -> None:

    logger.remove()
    logger.add(sys.stdout, serialize=ServiceConfig.json_log, format=_defaults.LOGURU_FORMAT + " | {extra}")
    logger.configure(extra={"service": ServiceConfig.name})

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True


setup_logging()
