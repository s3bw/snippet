<h1 align="center">
    Snippet
</h1>

<h4 align="center">
    Manage snippets for project development
</h4>

## Install

```
pip install snippet
```

## Usage

All usage is determined by the current directory.

Creates a new snippet.py. Will amend +=1 if exists.

```
snip new
```

Cleans snippets and logs them as a batch.

```
snip commit
```

List available batches.

```
snip list
```

Gets all snippets by batch id.

```
snip checkout <batch-id>
```

Updates a batch id with current snippets (if empty raise)

```
snip push <batch-id>
```

Edit latest snippet

```
snip edit
```

Delete a batch of snippets

```
snip delete <batch-id>
```
