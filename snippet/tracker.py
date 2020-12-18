import os
import ast
import glob
from pathlib import PurePath
from datetime import datetime


_WARNING = "\033[93m"
_ENDC = "\033[0m"


class Info:
    def __init__(self, snippet: str):
        self.name = snippet

        with open(snippet) as file:
            content = file.read()

        self.header = ast.get_docstring(ast.parse(content))
        timestamp = os.stat(snippet).st_birthtime
        self.created = datetime.utcfromtimestamp(timestamp).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def __str__(self):
        return f"{_WARNING}=> {self.name} - {self.created}{_ENDC}\n{self.header}\n"

    def todict(self):
        return {
            "name": self.name,
            "created": self.created,
            "header": self.header,
        }


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

    def snippet_info(self, snippet: str):
        """Returns info on snippet.

        :param snippet: Name of snippet.
        """
        return Info(snippet)

    def total_snippets(self):
        """ Count 'snippet\\d.py' in current dir."""
        return len(self.snippets())

    def snippets(self):
        return glob.glob(self.pattern)
