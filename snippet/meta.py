import json

from snippet.serializer import DateTimeDecoder
from snippet.serializer import DateTimeEncoder


class Meta:
    def __init__(self, date, hash, message, files):
        self.date = date
        self.hash = hash
        self.message = message
        self.files = files

    def update(self, message, files):
        self.message = message
        self.files = files

    def __str__(self):
        return (
            f"{self.date:%Y-%m-%d %H:%M:%S} - count: {self.files} - {self.hash}\n"
            f"  {self.message}\n")

    def to_json(self):
        return save({
            "date": self.date,
            "message": self.message,
            "files": self.files,
            "hash": self.hash,
        })


def load(content):
    meta = json.loads(content, cls=DateTimeDecoder)
    return Meta(**meta)


def save(dictionary):
    return json.dumps(dictionary, sort_keys=True, cls=DateTimeEncoder)
