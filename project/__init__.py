from .module_log import init_logger
from .module_log import set_logger as _set_logger

logger = init_logger(__name__)


def set_logger(**kwargs):
    _set_logger(logger, **kwargs)


from .project import *
