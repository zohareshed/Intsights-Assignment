from attr import dataclass
import datetime
import json


@dataclass
class PasteModel:
    paste_id: str
    author: str
    title: str
    content: str
    date: datetime.datetime

    def get_info_json(self):
        return json.dumps({
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "date": self.date
        }, default=str)
