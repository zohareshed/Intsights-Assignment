import logging
import sys

from crawler.crawler import Crawler
from config import LOGGING_FORMAT

if __name__ == '__main__':
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOGGING_FORMAT)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    cr = Crawler("https://pastebin.com")
    cr.run()
