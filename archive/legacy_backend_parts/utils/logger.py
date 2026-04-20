import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file="application.log", level=logging.INFO):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a file handler that logs even debug messages
    fh = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
    fh.setLevel(level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(fh)

    return logger
