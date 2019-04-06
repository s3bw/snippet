import shutil
from pathlib import Path

import click
from vim_edit import editor

from snippet.tracker import Tracker
from snippet.storage import Storage


def initialise():
    return Storage(), Tracker()


@click.command()
def status():
    store, track = initialise()
    print(f"Currently {track.count} snippets:")
    for snippet in track.snippets():
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

    # Currently prints snippet names in folder
    # this needs to traverse previous commits
    # and provide information on historical
    # snippet commits. Ordered by date
    store.list(store.namespace_path(namespace))


@click.command()
@click.argument("message", required=True)
def commit(message):
    store, track = initialise()
    namespace = track.dir.name
    if track.total_snippets() < 1:
        raise Exception("No snippets to commit")
    # Maybe instead of hash have the datetime?
    # Or have it be a branch-like name?
    hashname = "HASH"
    store.check_exists(store.commit_path(namespace, hashname))

    for snippet in track.snippets():
        shutil.move(snippet, store.snippet_path(namespace, hashname, snippet))
    print(message)
    # Write to commit meta.json (date, message, number of snippets)


@click.command()
@click.argument("commit_sha", required=True)
def checkout(commit_sha):
    """ pull specific commit."""
    store, track = initialise()
    namespace = track.dir.name

    path = Path(store.commit_path(namespace, commit_sha))
    if not path.exists():
        raise Exception("Commit doesn't exist")

    for snippet in store.list(path):
        if Path(track.dir, snippet).exists():
            raise Exception("Pull will overwrite {snippet}")

    for snippet in store.list(path):
        from_file = path / snippet
        to_file = track.dir / snippet
        shutil.copy2(from_file, to_file)

    print("Pull Completed")


@click.command()
@click.argument("commit_sha", required=True)
def push(commit_sha):
    """ update specific commit."""
    store, track = initialise()
    namespace = track.dir.name
    path = Path(store.commit_path(namespace, commit_sha))
    if not path.exists():
        raise Exception("Can not push to a commit that doesn't exist")
    # Print are you sure??

    # Delete snippets in HASH
    # Open meta for editing
    for snippet in track.snippets():
        from_file = track.dir / snippet
        to_file = path / snippet
        shutil.move(from_file, to_file)
    print("Push complete")


@click.command()
@click.argument("commit_sha", required=True)
def delete(commit_sha):
    """ delete specific commit."""
    store, track = initialise()
    namespace = track.dir.name
    path = Path(store.commit_path(namespace, commit_sha))
    if not path.exists():
        raise Exception("Can not delete a commit that doesn't exist")
    # Print are you sure??
    # Delete snippets in HASH including meta


@click.group()
def cli():
    pass


def main():
    cli.add_command(new)
    cli.add_command(edit)
    cli.add_command(commit)
    cli.add_command(log)
    cli.add_command(status)
    cli.add_command(checkout)
    cli.add_command(push)
    cli.add_command(delete)
    cli()
