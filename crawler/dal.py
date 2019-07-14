import os
import logging

from crawler.paste_model import PasteModel
from crawler.exceptions.failed_to_make_dir_error import FailedToMakeDirError


class PasteDal(object):
    def __init__(self, root_directory):
        self.logger = logging.getLogger(__name__)
        if not os.path.isdir(root_directory):
            try:
                os.makedirs(root_directory)
            except Exception as e:
                self.logger.critical(f"Failed to create a dir in the path {root_directory}, terminating.")
                raise FailedToMakeDirError(str(e))
        self.root_directory = root_directory

    def is_paste_saved(self, paste_id: str) -> bool:
        dirlist = os.listdir(self.root_directory)
        if paste_id in dirlist:
            return True
        return False

    def save_paste(self, paste: PasteModel):
        file_path = os.path.join(self.root_directory, paste.paste_id)
        with open(file_path, "w") as fp:
            fp.write(paste.get_info_json())
