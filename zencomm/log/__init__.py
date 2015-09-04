import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('zen')
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

from logging.handlers import RotatingFileHandler
# handler2: to log file
logfile = '/var/log/zen.log'
filehandler = RotatingFileHandler(logfile,
                                  mode='a',
                                  maxBytes=100000000,
                                  backupCount=3)
filehandler.setFormatter(formatter)


# handler.setFormatter(formatter)
# logger.addHandler(handler)
logger.addHandler(filehandler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info('test logger_info')
    logger.warn('test logger_warn')
    logger.error('test logger_error')
    logger.debug('test logger_debug')
