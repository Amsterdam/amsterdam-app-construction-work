import logging
import os


class Logger:
    """ Central logging system. If the environment DEBUG is set, all logging will be printed to the console else it will
        be send to the operating-system its logging facility.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.debug_enabled = os.getenv('DEBUG', 'false').lower() == 'true'

    def info(self, record):
        if self.debug_enabled is True:
            print(record)
        else:
            self.logger.info(record)

    def error(self, record):
        if self.debug_enabled is True:
            print(record)
        else:
            self.logger.error(record)

    def debug(self, record):
        if self.debug_enabled is True:
            print(record)
        else:
            self.logger.debug(record)
