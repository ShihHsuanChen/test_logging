# from loghandler import loghandler
from loghandler import MyLogHandler


loghandler = MyLogHandler(__name__)


def set_logger(**kwargs):
    loghandler.set_logger(loghandler.root_name, **kwargs)


def test():
    loghandler.logger.info('test-1')
    test1()
    loghandler.logger.info('test-2')


@loghandler.scoped()
def test1():
    # logging.info('foo2-1')
    loghandler.logger.info('test1')
