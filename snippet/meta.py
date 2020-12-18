import json

from snippet.serializer import DateTimeDecoder
from snippet.serializer import DateTimeEncoder

_GREEN = "\033[92m"
_ENDC = "\033[0m"


class Meta:
    def __init__(self, date, hash, message, count):
        self.date = date
        self.hash = hash
        self.message = message
        self.count = count

    def update(self, message, count):
        self.message = message
        self.count = count

    def __str__(self):
        message = "\n\t".join(self.message.split("\n"))
        return (
            f"{_GREEN}Commit: {self.hash}\n{_ENDC}"
            f"Number of files: {self.count}\n"
            f"Date: {self.date:%a %b %d %H:%M:%S %Y}\n\n"
            f"\t{message}\n"
        )

    def to_json(self):
        return save(
            {
                "date": self.date,
                "message": self.message,
                "count": self.count,
                "hash": self.hash,
            }
        )


def load(content):
    meta = json.loads(content, cls=DateTimeDecoder)
    return Meta(**meta)


def save(dictionary):
    return json.dumps(dictionary, sort_keys=True, cls=DateTimeEncoder)
