import os
import glob
from pathlib import PurePath
from datetime import datetime


class Tracker:
    """Should I manage snippets in a separate dir?"""

    pattern = "snippet*.py"

    def __init__(self):
        self.dir = PurePath(os.getcwd())
        self.count = self.total_snippets()

    def next_snippet(self):
        self.count += 1
        return f"snippet{self.count}.py"

    def snippet(self):
        return f"snippet{self.count}.py"

    def snippet_info(self, snippet):
        info = os.stat(snippet)
        timestamp = info.st_birthtime
        created = datetime.utcfromtimestamp(timestamp).strftime(
            '%Y-%m-%d %H:%M:%S')
        return {
            'name': snippet,
            'created': created,
        }

    def total_snippets(self):
        """ Count 'snippet\\d.py' in current dir."""
        return len(self.snippets())

    def snippets(self):
        return glob.glob(self.pattern)
