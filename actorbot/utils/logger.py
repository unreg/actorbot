from logging import getLogger, StreamHandler, Formatter, DEBUG, WARNING, INFO
from logging.handlers import RotatingFileHandler

import sys
import os

logger = getLogger(__package__)

class ColorFormatter(Formatter):
    """
    """
    black, red, green, yellow, blue, magenta, cyan, white = range(8)
    colors = {
        'WARNING': yellow,
        'INFO': green,
        'DEBUG': white,
        'CRITICAL': yellow,
        'ERROR': red,
        'RED': red,
        'GREEN': green,
        'YELLOW': yellow,
        'BLUE': blue,
        'MAGENTA': magenta,
        'CYAN': cyan,
        'WHITE': white
    }
    reset_seq = '\033[0m'
    color_seq = '\033[%dm'
    bold_seq = '\033[1m'

    def format(self, record):
        """Format the record with colors."""
        color = self.color_seq % (30 + self.colors[record.levelname])
        message = Formatter.format(self, record)
        message = message.replace('$RESET', self.reset_seq)\
            .replace('$BOLD', self.bold_seq)\
            .replace('$COLOR', color)
        for color, value in self.colors.items():
            message = message.replace(
                '$' + color, self.color_seq % (value + 30))\
                .replace('$BG' + color, self.color_seq % (value + 40))\
                .replace('$BG-' + color, self.color_seq % (value + 40))
        return message + self.reset_seq

def logger_init(stream_log_level=WARNING, colorized=False):
    """
    """
    logger.setLevel(DEBUG)

    stream_handler = StreamHandler(sys.stderr)
    formatter = Formatter(
        '[%(levelname).1s] [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if colorized:
        c_formatter = ColorFormatter(
            ('$RESET$COLOR[%(levelname).1s]$RESET %(asctime)s '
             '$BOLD$COLOR[%(name)s:%(filename)s:%(funcName)s:%(lineno)d] '
             '$RESET%(message)s'))
        stream_handler.setFormatter(c_formatter)
    else:
        stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_log_level)
    logger.addHandler(stream_handler)

    return logger
