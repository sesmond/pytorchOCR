import logging


def init():
    level = logging.DEBUG
    logging.basicConfig(
        format='%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d行： %(message)s',
        level=level,
        handlers=[logging.StreamHandler()])
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
