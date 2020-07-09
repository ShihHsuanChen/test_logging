from . import logger


print(__name__)


class Project:
    def __init__(self):
        logger.info('create Project')


def project_manage():
    logger.info('project_manage')
    p = Project()
    return p
