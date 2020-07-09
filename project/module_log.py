import logging
from sys import stdout
from logging import Formatter
from logging import FileHandler
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler


default_format_str = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
default_formatter = Formatter(default_format_str)
default_level = logging.INFO


def init_logger(name, **kwargs):
    logger = logging.getLogger(name)
    set_logger(logger, **kwargs)
    return logger


def set_logger(logger, format_str=default_format_str, filename=None, level=default_level, **kwargs):
    logger.setLevel(level)
    formatter = Formatter(format_str)

    console_handler = StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    _remove_handlers(logger)
    logger.addHandler(console_handler)

    if filename is not None:
        file_handler = _get_file_handler(filename, **kwargs)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def _get_file_handler(filename, when=None, interval=1, backupCount=0):
    # set to current logger
    if when is None:
        file_handler = FileHandler(filename, 'a', 'utf-8')
    else:
        file_handler = TimedRotatingFileHandler(
            filename,
            encoding='utf-8',
            when=when,
            interval=interval,
            backupCount=backupCount
            )
    return file_handler


def _remove_handlers(logger):
    for h in logger.handlers:
        logger.removeHandler(h)
