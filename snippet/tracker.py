"""Tracks snippets in the local directory."""
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
        header = "" if not self.header else f"{self.header}\n"
        return f"{_WARNING}=> {self.name} - {self.created}{_ENDC}\n{header}"

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
        self.directory = PurePath(os.getcwd())
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


_instance = Tracker()

snippet = _instance.snippet
snippets = _instance.snippets
snippet_info = _instance.snippet_info
next_snippet = _instance.next_snippet
directory = _instance.directory
count = _instance.count
total_snippets = _instance.total_snippets
