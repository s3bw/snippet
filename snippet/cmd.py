import os
import glob
from datetime import datetime
from pathlib import PurePath, Path

import click
from vim_edit import editor


class Storage:

    root = Path.home()

    def namespace_path(self, namespace):
        return f"{self.root}/.snippets/{namespace}/"

    def commit_path(self, namespace, commit):
        """ Batches are tagged at creation."""
        return f"{self.root}/.snippets/{namespace}/{commit}/"

    def commit_info(self, namespace, commit):
        return f"{self.root}/.snippets/{namespace}/{commit}/meta.json"

    def check_exists(self, folder):
        print(folder)
        # Path(folder).mkdir(parents=True, exist_ok=True)

    def list(self, folder):
        self.check_exists(folder)
        for file in os.listdir(folder):
            print(file)


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
        return len(self.all_snippets())

    def all_snippets(self):
        return glob.glob(self.pattern)


def initialise():
    return Storage(), Tracker()


@click.command()
def status():
    store, track = initialise()
    print(f"Currently {track.count} snippets:")
    for snippet in track.all_snippets():
        info = track.snippet_info(snippet)
        # Order Snippets
        print(f"  >   {info['name']} - {info['created']}")


@click.command()
def new():
    store, track = initialise()
    snippet_name = track.next_snippet()

    with open(snippet_name, 'x') as file:
        editor.open(file)
    print("Snippet created.")


@click.command()
def edit():
    store, track = initialise()
    snippet_name = track.snippet()

    with open(snippet_name, 'r') as file:
        editor.open(file)
    print("Edited.")


@click.command()
def log():
    store, track = initialise()
    namespace = track.dir.name

    store.list(store.namespace_path(namespace))


@click.command()
@click.argument("message")
def commit(message):
    store, track = initialise()
    namespace = track.dir.name
    hashname = "HASH"

    path = store.commit_path(namespace, hashname)
    # store.check_exists(path)
    # Move from current directory -> commit path
    # Write to commit meta.json (date, message, number of snippets)


def pull(batch_id):
    """ pull specific commit."""
    pass


def push(batch_id):
    """ update specific commit."""
    pass


def delete(batch_id):
    """ delete specific commit."""
    pass


@click.group()
def cli():
    pass


def main():
    cli.add_command(new)
    cli.add_command(edit)
    cli.add_command(commit)
    cli.add_command(list)
    cli.add_command(status)
    # cli.add_command(pull)
    cli()
