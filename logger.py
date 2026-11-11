import logging
import colorlog
import sys


def setup_logger():
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)

    log_colors = {
        'DEBUG': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'purple',
    }

    formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(asctime)s] %(levelname)-8s %(filename)s: %(lineno)d - %(message)s',
        log_colors=log_colors
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()