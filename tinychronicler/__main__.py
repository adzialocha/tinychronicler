import logging
import os
import sys

import click
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


def setup_server(host: str, port: int):
    config = Config(
        "tinychronicler:server",
        host=host,
        port=port,
        log_level=LOG_LEVEL,
    )
    server = Server(config=config)
    return server


@click.command()
@click.option(
    "--host",
    type=str,
    default="0.0.0.0",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
def main(host: str, port: int):
    # Start HTTP server hosting web interface for users
    server = setup_server(host, port)

    # Set up logging after server setup to make sure it overrides everything
    setup_logging()

    # Start server and block thread from here on
    server.run()


if __name__ == "__main__":
    main()
