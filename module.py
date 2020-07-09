import logging
from loghandler import loghandler as lh
from loghandler import MyLogHandler
from module2.module2 import test
from module2.module2 import set_logger as module2_set_logger


loghandler = MyLogHandler(__name__)


def set_logger(**kwargs):
    loghandler.set_logger(loghandler.root_name, **kwargs)
    module2_set_logger(**kwargs)


def foo():
    lh.logger.info('foo-1')
    lh.logger.info('foo-2')


# @loghandler.scoped('mymodel.foo1')
@loghandler.scoped()
def foo1():
    loghandler.logger.info('foo1-1')
    foo2()
    loghandler.logger.info('foo1-2')


@loghandler.scoped()
def foo2():
    loghandler.logger.info('foo2-2')
    test()
