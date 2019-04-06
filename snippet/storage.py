import os
from pathlib import Path


class Storage:

    root = Path.home()

    def namespace_path(self, namespace):
        return f"{self.root}/.snippets/{namespace}/"

    def commit_path(self, namespace, commit):
        """ Batches are tagged at creation."""
        return f"{self.root}/.snippets/{namespace}/{commit}/"

    def commit_info(self, namespace, commit):
        return f"{self.root}/.snippets/{namespace}/{commit}/meta.json"

    def snippet_path(self, namespace, commit, snippet):
        return f"{self.root}/.snippets/{namespace}/{commit}/{snippet}"

    def check_exists(self, folder):
        print(folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    def list(self, folder):
        self.check_exists(folder)
        for file in os.listdir(folder):
            print(file)
            yield file
