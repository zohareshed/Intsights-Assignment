RECENT_PASTES_URL = "/archive"
ROOT_DIRECTORY = "C:/Code/Pastes"
MAIN_LOOP_RUNNING_INTERVAL_IN_SECONDS = 120.0
HTTP_REQUEST_INTERVAL_IN_SECONDS = 1
GUEST_AUTHOR = "A GUEST"
PASTE_DATE_FORMAT = "%b %dth, %Y"
LOGGING_FORMAT = '%(asctime)s  %(levelname)-10s %(name)s %(message)s'


class HtmlXPaths:
    PASTE_LINK_XPATH = "//*/img[@class='i_p0']/../a/@href"
    PASTE_GUEST_AUTHOR_XPATH = "//*/div[@class='paste_box_line2']/text()"
    PASTE_USER_AUTHOR_XPATH = "//*/div[@class='paste_box_line2']/a"
    PASTE_TITLE_XPATH = "//*/div[@class='paste_box_line1']/h1/text()"
    PASTE_CONTENT_XPATH = "//*/textarea[@id='paste_code']/text()"
    PASTE_DATE_XPATH = "//*/div[@class='paste_box_line2']/span/text()"
    PASTE_EMAIL_ICON_XPATH = "//*/img[@class='i_pm']"
