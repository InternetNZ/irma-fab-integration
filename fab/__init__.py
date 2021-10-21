"""
IRMA - FAB Integration
"""
import logging

# Setting up the logger
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info('Starting FAB-IRMA Integration Backend.')


class InternalServerError(Exception):
    """
    Internal server error class.
    """

    def __init__(self, description=None, code=None):
        Exception.__init__(self)
        self.description = description if description else \
            "Something bad happened on the server! Check the server logs for more details!"
        self.code = code if code else 500
        self.name = "Internal Server Error"
