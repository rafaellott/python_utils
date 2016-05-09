"""Source http://www.blog.pythonlibrary.org/2014/02/11/python-how-to-create-rotating-logs/"""
from logging.handlers import TimedRotatingFileHandler
import logging


def create_timed_rotating_log(path_log, when="midnight", last=3, interval=1):
    """Create a log based on TimedRotatingFileHandler."""
    logger = logging.getLogger("Test rotating file")
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    if path_log:
        hdlr = TimedRotatingFileHandler(
            path_log, when=when, interval=interval, backupCount=last
        )
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.debug("[LOG] Criou arquivo de log")
    else:
        hdlr2 = logging.StreamHandler()
        hdlr2.setFormatter(formatter)
        logger.addHandler(hdlr2)
    return logger
