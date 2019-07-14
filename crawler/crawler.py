import datetime
import logging
import time

from crawler.paste_model import PasteModel
from crawler.dal import PasteDal
from crawler.exceptions.failed_to_extarct_data_from_paste_error import FailedToExtractDataFromPasteException
from config import HtmlXPaths
import config
from crawler import utils


class Crawler(object):
    def __init__(self, site: str, root_directory: str):
        self.site = site
        self.dal = PasteDal(root_directory)
        self.logger = logging.getLogger(__name__)

    def _get_full_paste(self, paste_link: str) -> PasteModel:
        paste_id = paste_link[1:]  # Remove the "/" from the url.
        full_link = self.site + paste_link
        author = self._get_author(full_link)
        try:
            title = self._get_title(full_link)
            content = self._get_content(full_link)
            date = self._get_date(full_link)
            return PasteModel(paste_id, author, title, content, date)
        except IndexError:
            raise FailedToExtractDataFromPasteException

    @staticmethod
    def _get_title(full_link: str) -> str:
        return utils.get_html_data_with_xpath(full_link, HtmlXPaths.PASTE_TITLE_XPATH)[0].title()

    @staticmethod
    def _get_content(full_link: str) -> str:
        return utils.get_html_data_with_xpath(full_link, HtmlXPaths.PASTE_CONTENT_XPATH)[0].title()

    @staticmethod
    def _get_author(full_link: str) -> str:
        author = utils.get_html_data_with_xpath(full_link, HtmlXPaths.PASTE_USER_AUTHOR_XPATH)
        if not len(author):  # If the author's name doesn't exists, it's a guest.
            return config.GUEST_AUTHOR
        return author[0].text

    @staticmethod
    def _get_date(full_link: str) -> datetime.datetime:
        raw_date = utils.get_html_data_with_xpath(full_link, HtmlXPaths.PASTE_DATE_XPATH)[0].title()
        return datetime.datetime.strptime(raw_date, config.PASTE_DATE_FORMAT)

    def _handle_paste(self, paste_link: str):
        self.logger.info(f"Getting the paste: {paste_link}")
        paste_id = paste_link[1:]  # Remove the "/" from the url.
        if self.dal.is_paste_saved(paste_id):
            self.logger.info(f"Paste already exits: {paste_link}")
            return
        try:
            paste = self._get_full_paste(paste_link)
            self.dal.save_paste(paste)
            self.logger.info(f"Paste saved successfully! {paste_link}")
        except FailedToExtractDataFromPasteException as e:
            self.logger.error(f"Failed to extract the paste {paste_link}\r\n info: {str(e)}")
        except Exception as e:
            self.logger.error(f"Something went wrong with the paste: {paste_link}\r\n info: {str(e)}")
        finally:
            return

    def _handle_pastes_links(self, pastes_links: list):
        for link in pastes_links:
            self._handle_paste(link)
            time.sleep(config.HTTP_REQUEST_INTERVAL_IN_SECONDS)

    def run(self):
        """
        This method runs every 2 minutes and grabs a paste every 1 seconds - due to the website restrictions.
        :return:
        """
        start_time = time.time()
        while True:
            self.logger.info("Getting pastes links")
            full_link = self.site + config.RECENT_PASTES_URL
            pastes_links = utils.get_html_data_with_xpath(full_link, HtmlXPaths.PASTE_LINK_XPATH)
            self._handle_pastes_links(pastes_links)

            time_diff_from_last_run = config.MAIN_LOOP_RUNNING_INTERVAL_IN_SECONDS - (
                    (time.time() - start_time) % config.MAIN_LOOP_RUNNING_INTERVAL_IN_SECONDS)
            if time_diff_from_last_run > 0:
                time.sleep(time_diff_from_last_run)
