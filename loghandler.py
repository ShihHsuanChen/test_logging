import logging
from sys import stdout
from functools import wraps
from logging import FileHandler
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from logging import RootLogger


''' default setting '''
default_format_str = '%(asctime)s #%(thread)d [%(levelname)s] [%(name)s] %(message)s'
default_formatter = logging.Formatter(default_format_str)

default_level = logging.INFO


class MyLogHandler:

    def __init__(self, root_name: str = None):
        self.logger = None
        root_name = root_name if root_name is not None else str(hex(id(root_name)))
        self._root_name = root_name
        self._set_logger(root_name)

    @property
    def root_name(self):
        return self._root_name

    @property
    def _root_logger(self):
        return logging.getLogger(self._root_name)

    @_root_logger.setter
    def _root_logger(self, logger):
        self._root_name = logger.name
        self._root_handlers = [*logger.handlers]

    def get_root_name(self):
        return self._root_name

    def get_root_logger(self):
        return logging.getLogger(self._root_name)

    def set_path(self, filename, level=default_level, when=None, interval=1, backupCount=0):
        # set to current logger
        file_handler = get_file_handler(filename, when=when, interval=interval, backupCount=backupCount)
        console_handler = StreamHandler(stdout)
        console_handler.setFormatter(default_formatter)

        _remove_handlers(self.logger)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def set_logger(self, name, **kwargs):
        _name = f'{self._root_name}.{name}'
        self._set_logger(_name, **kwargs)

    def _set_logger(self, name, level=default_level, handlers=None, format: str=None, filename: str=None, when=None, interval=1, backupCount=0, inherit=True):

        logger = logging.getLogger(name)
        logger.propagate = False

        is_root = isinstance(logger.parent, RootLogger)
        default_console_handler = StreamHandler(stdout)
        default_console_handler.setFormatter(default_formatter)

        logging._acquireLock()
        try:
            if handlers is None and filename is None and format is None:
                if is_root or not inherit:
                    _handlers = [default_console_handler]
                    # print(name, _handlers[0].formatter)
                elif len(logger.handlers) == 0:
                    if len(logger.parent.handlers) == 0:
                        _handlers = [*self._root_handlers]
                    else:
                        _handlers = [*logger.parent.handlers]
                else:
                    _handlers = [*logger.handlers]
            elif handlers is None:
                # handlers
                if not inherit:
                    _handlers = [default_console_handler]
                elif len(logger.handlers) == 0:
                    if len(logger.parent.handlers) == 0:
                        _handlers = [*self._root_handlers]
                    else:
                        _handlers = [*logger.parent.handlers]
                else:
                    _handlers = [*logger.handlers]

                if filename is not None:
                    file_handler = get_file_handler(filename, when=when, interval=interval, backupCount=backupCount)
                    _handlers.append(file_handler)

                # formatters
                if format is not None:
                    formatter = logging.Formatter(format)
                elif not inherit:
                    formatter = default_formatter
                elif len(logger.handlers) > 0:
                    formatter = logger.handlers[0].formatter
                elif len(logger.parent.handlers) > 0:
                    formatter = logger.parent.handlers[0].formatter
                else:
                    # print(self._root_name, self._root_handlers)
                    formatter = self._root_handlers[0].formatter

                # combine
                for h in _handlers:
                    h.setFormatter(formatter)
            else:
                _handlers = [*handlers]

            if level is not None:
                logger.setLevel(level)

            _set_handlers(logger, _handlers)
            self.logger = logger

            if is_root:
                self._root_logger = logger
        finally:
            logging._releaseLock()

    def scoped(self, name: str = None, **log_args):
        def _decorate(func):
            _name = name
            if _name is None:
                _name = f'{self._root_name}.{func.__qualname__}'

            @wraps(func)
            def decorator(*args, **kwargs):
                prev_name = self.logger.name
                prev_handlers = self.logger.handlers
                # print(prev_name, prev_handlers)

                self.set_logger(_name, **log_args)

                res = func(*args, **kwargs)

                self.set_logger(prev_name, handlers=prev_handlers)
                return res
            return decorator
        return _decorate


def _set_handlers(logger, handlers):
    _remove_handlers(logger)
    for h in handlers:
        logger.addHandler(h)


def _remove_handlers(logger):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    for h in logger.handlers:
        logger.removeHandler(h)


def get_file_handler(filename, when=None, interval=1, backupCount=0):
    # set to current logger
    if when is None:
        file_handler = FileHandler(filename, 'a', 'utf-8')
    else:
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename,
            encoding='utf-8',
            when=when,
            interval=interval,
            backupCount=backupCount
            )
    return file_handler

loghandler = MyLogHandler('default')
