import logging


class CustomFormatter(logging.Formatter):
    # Define the custom format for log messages
    FORMAT = "[%(asctime)s][%(levelname)8s][%(name)8s]:%(message)s"

    def __init__(self):
        super().__init__(self.FORMAT, datefmt="%Y-%m-%d %H:%M:%S")


def setup_logger(name, level=logging.DEBUG):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Set the custom formatter
    ch.setFormatter(CustomFormatter())

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    logger.propagate = False
    return logger
