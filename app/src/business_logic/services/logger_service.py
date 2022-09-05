import logging
import logging.config
from os import path


class Logger:
    def __init__(
            self,
            log_file_path=path.join(path.dirname(path.abspath(__file__)), '../../config/logging.conf')
    ):
        logging.config.fileConfig(log_file_path)
        self.logger = logging.getLogger()

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)
