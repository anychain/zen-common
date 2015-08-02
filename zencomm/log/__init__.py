import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('zen')
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('test logger_info')
    logger.warn('test logger_warn')
    logger.error('test logger_error')
    logger.debug('test logger_debug')
