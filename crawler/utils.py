import requests
import lxml.html

from crawler.exceptions.site_unreachable_error import SiteUnreachableError


def get_html_data_with_xpath(link: str, xpath: str) -> list:
    try:
        html_content = requests.get(link).content
    except Exception:
        raise SiteUnreachableError
    lxml_doc = lxml.html.fromstring(html_content)
    return lxml_doc.xpath(xpath)
