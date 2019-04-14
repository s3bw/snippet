<h1 align="center">
    Snippet-Manager
</h1>

<h4 align="center">
    Manage snippets for project development
</h4>

## Install

```
pip install snippet-manager
```

## Usage

All usage is determined by the current directory.

Creates a new snippet.py. Will amend +=1 if exists.

```
snip new
```

Edit latest snippet

```
snip edit
```

Cleans snippets and logs them as a batch.

```
snip commit
```

List available batches of snippets.

```
snip log
```

Gets all snippets by batch sha.

```
snip checkout <batch-sha>
```

Updates a batch sha with current snippets (if empty raise)

```
snip update <batch-sha>
```

Delete a batch of snippets

```
snip delete <batch-sha>
```
