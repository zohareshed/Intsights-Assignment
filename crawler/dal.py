import os

from crawler.paste_model import PasteModel


class PasteDal(object):
    def __init__(self, root_directory):
        if not os.path.isdir(root_directory):
            os.makedirs(root_directory)
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
