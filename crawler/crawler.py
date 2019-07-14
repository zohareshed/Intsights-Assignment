import requests
import lxml.html
import threading
import datetime
import logging

from crawler.paste_model import PasteModel
from crawler.dal import PasteDal
from crawler.exceptions.failed_to_extarct_data_from_paste_exception import FailedToExtractDataFromPasteException
from config import HtmlXPaths
import config


class Crawler(object):
    def __init__(self, site: str):
        self.site = site
        self.dal = PasteDal(config.ROOT_DIRECTORY)
        self.logger = logging.getLogger(__name__)

    def _get_data_with_xpath(self, link: str, xpath: str) -> list:
        html_content = requests.get(self.site + link).content
        lxml_doc = lxml.html.fromstring(html_content)
        return lxml_doc.xpath(xpath)

    def _get_full_paste(self, paste_link: str) -> PasteModel:
        paste_id = paste_link[1:]  # Remove the / from the url.
        author = self._get_author(paste_link)
        try:
            title = self._get_data_with_xpath(paste_link, HtmlXPaths.PASTE_TITLE_XPATH)[0].title()
            content = self._get_data_with_xpath(paste_link, HtmlXPaths.PASTE_CONTENT_XPATH)[0].title()
            date = self._get_date(paste_link)
            return PasteModel(paste_id, author, title, content, date)
        except IndexError:
            raise FailedToExtractDataFromPasteException

    def _get_author(self, paste_link: str) -> str:
        author = self._get_data_with_xpath(paste_link, HtmlXPaths.PASTE_USER_AUTHOR_XPATH)
        if not len(author):  # If the author's name doesn't exists, it's a guest.
            return config.GUEST_AUTHOR
        return author[0].text

    def _get_date(self, paste_link: str) -> datetime.datetime:
        raw_date = self._get_data_with_xpath(paste_link, HtmlXPaths.PASTE_DATE_XPATH)[0].title()
        return datetime.datetime.strptime(raw_date, config.PASTE_DATE_FORMAT)

    def _handle_paste(self, paste_link: str):
        paste_id = paste_link[1:]  # Remove the / from the url.
        if self.dal.is_paste_saved(paste_id):
            return
        try:
            paste = self._get_full_paste(paste_link)
            self.dal.save_paste(paste)
            self.logger.info(f"Paste saved successfully! {paste_link}")
        except FailedToExtractDataFromPasteException as e:
            self.logger.error(f"Failed to extract the paste {paste_link}\r\n info: {str(e)}")
            return
        except Exception as e:
            self.logger.error(f"Something went wrong with the paste: {paste_link}\r\n info: {str(e)}")
            return

    def run(self):
        threading.Timer(config.MAIN_LOOP_RUNNING_INTERVAL_IN_SECONDS, self.run).start()
        self.logger.info("Getting pastes links")
        pastes_links = self._get_data_with_xpath(config.RECENT_PASTES_URL, HtmlXPaths.PASTE_LINK_XPATH)
        for link in pastes_links:
            self.logger.info(f"Getting the paste: {link}")
            self._handle_paste(link)
