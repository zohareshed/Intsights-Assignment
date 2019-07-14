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

    try:
        root_directory = sys.argv[1]
    except IndexError:
        print("Please add a root directory: main.py <root_directory>")
        sys.exit(1)
    cr = Crawler("https://pastebin.com", root_directory)
    cr.run()
