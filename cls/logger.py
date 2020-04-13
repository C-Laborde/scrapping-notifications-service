import logging


class Logger:
    def __init__(self):
        logging.basicConfig(level="INFO")
        self.logger = logging.getLogger(__name__)