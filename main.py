import logging
from sys import stdout
from loghandler import MyLogHandler
from loghandler import loghandler as lh
from module import foo, foo1, foo2
from module import set_logger as module_set_logger


loghandler = MyLogHandler('main')


def run():
    # change log path by set_logger()
    loghandler.set_logger('run', filename='./testlog1.log')
    loghandler.logger.info('start')
    loghandler.set_logger('run', filename='./testlog2.log')
    loghandler.logger.info('end')


def run1():
    lh.set_logger('main1', format='[%(name)s] %(message)s', filename='./testlog.log', level=20)
    # print(logging.getLogger('default.main1').handlers)
    lh.logger.info('start')
    # print(logging.getLogger('default.main1').handlers)
    lh.set_logger('run1', filename='./testlog_foo.log')
    # print(logging.getLogger('default.main1').handlers)
    foo()
    lh.set_logger('main1')
    # print(logging.getLogger('default.main1').handlers)
    lh.logger.info('end')


def run2():
    loghandler.logger.info('start')
    print('module_set_logger')
    module_set_logger(format='[%(name)s] %(message)s', filename='./testlog_foo1.log')
    foo1()
    loghandler.logger.info('end')


def run3():
    loghandler.set_logger('run1')
    loghandler.logger.info('start')
    # foo2()
    # print('=======')
    # foo1()
    # print('=======')
    foo2()
    loghandler.logger.info('end')

    
if __name__ == '__main__':
    # run()
    run1()
    # run2()
