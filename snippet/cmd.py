import uuid
import shutil
from pathlib import Path
from datetime import datetime

import click
from vim_edit import editor

from snippet import meta
from snippet.meta import Meta
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

    logs = []
    for file_name in store.list(store.namespace_path(namespace)):
        file_path = store.meta_path(namespace, file_name)
        logs.append(meta.load(store.read(file_path)))

    if not logs:
        print(f"No snippets for namespace: '{namespace}'")
        exit()

    logs = sorted(logs, key=lambda x: x.date)
    for info in logs:
        print(info)


@click.command()
@click.argument("message", required=True)
def commit(message):
    store, track = initialise()
    namespace = track.dir.name
    date = datetime.now()

    if track.total_snippets() < 1:
        raise Exception("No snippets to commit")

    commit_sha = str(uuid.uuid4())[:8]
    store.check_exists(store.commit_path(namespace, commit_sha))

    meta_data = Meta(date, commit_sha, message, track.total_snippets())
    store.write(store.meta_path(namespace, commit_sha), meta_data.to_json())
    for snippet in track.snippets():
        shutil.move(snippet, store.snippet_path(namespace, commit_sha,
                                                snippet))

    print(f"Written to commit: {commit_sha}")


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
            raise Exception(f"Pull will overwrite {snippet}")

    for snippet in store.list(path):
        from_file = path / snippet
        to_file = track.dir / snippet
        shutil.copy2(from_file, to_file)

    print("Pull Completed")


@click.command()
@click.argument("commit_sha", required=True)
@click.argument("message", required=False)
def update(commit_sha, message):
    """ update specific commit."""
    store, track = initialise()
    namespace = track.dir.name
    path = Path(store.commit_path(namespace, commit_sha))
    if not path.exists():
        raise Exception("Can not push to a commit that does not exist.")

    click.confirm(
        f"Update will overwrite the current contents of {commit_sha}, are you sure?",
        abort=True)

    file_path = store.meta_path(namespace, commit_sha)
    meta_data = meta.load(store.read(file_path))
    new_messge = message if message else meta_data.message
    meta_data.update(new_messge, track.total_snippets())

    store.delete(path)
    store.check_exists(store.commit_path(namespace, commit_sha))
    store.write(store.meta_path(namespace, commit_sha), meta_data.to_json())

    # Delete snippets in HASH
    # Open meta for editing
    for snippet in track.snippets():
        from_file = track.dir / snippet
        to_file = path / snippet
        shutil.move(from_file, to_file)
    print("Update complete")


@click.command()
@click.argument("commit_sha", required=True)
def delete(commit_sha):
    """ delete specific commit."""
    store, track = initialise()
    namespace = track.dir.name
    path = Path(store.commit_path(namespace, commit_sha))
    if not path.exists():
        raise Exception("Can not delete a commit that does not exist")

    click.confirm(
        f"Deleting will destroy the contents of {commit_sha}, are you sure?",
        abort=True)
    store.delete(path)


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
    cli.add_command(update)
    cli.add_command(delete)
    cli()
