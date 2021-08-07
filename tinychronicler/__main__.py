import logging
import os
import sys

from loguru import logger
from uvicorn import Config, Server

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Finally log the message
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])


def main():
    # Start HTTP server hosting web interface for users
    server = Server(
        Config(
            "tinychronicler:server",
            host="0.0.0.0",
            log_level=LOG_LEVEL,
        ),
    )

    # Log everything!
    setup_logging()

    # Start server and block thread from here on
    server.run()


if __name__ == "__main__":
    main()
