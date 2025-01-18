import logging
import sys

from better_backlight.config import ServiceConfig


def configure_logger(config: ServiceConfig) -> None:
    logging.basicConfig(
        level=config.logging.level.upper(),
        format="%(asctime)s [%(levelname)s] %(message)s",
        filename=config.logging.file,
    )

    # Add a StreamHandler to output logs to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.logging.level.upper())
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    logging.getLogger().addHandler(console_handler)
