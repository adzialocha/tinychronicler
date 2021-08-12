import logging
import sys

import click
from loguru import logger
from uvicorn import Config, Server

from . import models
from .constants import LOG_LEVELS
from .database import engine


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


def setup_logging(log_level: str):
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level.upper())

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])


def setup_server(host: str, port: int, log_level: str):
    config = Config(
        "tinychronicler:server",
        host=host,
        port=port,
        log_level=log_level,
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
@click.option(
    "--log-level",
    type=click.Choice(list(LOG_LEVELS.keys())),
    default="info",
    help="Log level.",
    show_default=True,
)
def main(host: str, port: int, log_level: str):
    # Run all migrations
    models.Base.metadata.create_all(bind=engine)

    # Start HTTP server hosting web interface for users
    server = setup_server(host, port, log_level)

    # Set up logging after server setup to make sure it overrides everything
    setup_logging(log_level)

    # Start server and block thread from here on
    server.run()
