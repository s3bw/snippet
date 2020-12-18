import os
import shutil
from pathlib import Path


class Storage:

    root = Path.home()

    def namespace_path(self, namespace):
        return f"{self.root}/.snippets/{namespace}/"

    def commit_path(self, namespace, commit):
        """ Batches are tagged at creation."""
        return f"{self.root}/.snippets/{namespace}/{commit}/"

    def meta_path(self, namespace, commit):
        return f"{self.root}/.snippets/{namespace}/{commit}/meta.json"

    def snippet_path(self, namespace, commit, snippet):
        return f"{self.root}/.snippets/{namespace}/{commit}/{snippet}"

    def write(self, path, data):
        with open(path, "w") as file:
            file.write(data)

    def read(self, path):
        with open(path, "r") as file:
            content = file.read()
        return content

    def delete(self, directory):
        shutil.rmtree(directory)

    def check_exists(self, folder):
        Path(folder).mkdir(parents=True, exist_ok=True)

    def list(self, folder):
        self.check_exists(folder)
        for file in os.listdir(folder):
            if file != "meta.json":
                yield file


_instance = Storage()

namespace_path = _instance.namespace_path
meta_path = _instance.meta_path
read = _instance.read
check_exists = _instance.check_exists
commit_path = _instance.commit_path
snippet_path = _instance.snippet_path
list = _instance.list
delete = _instance.delete
write = _instance.write
