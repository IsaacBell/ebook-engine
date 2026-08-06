# CLI Reference

## `ebook-engine init [path]`

Create a new `ebook.toml` in the current directory or at `path`.

```bash
ebook-engine init
ebook-engine init my-book/
```

## `ebook-engine build [path]`

Build a book from its `ebook.toml`.

```bash
ebook-engine build .
ebook-engine build ./my-book/
```

The command auto-detects the source type:

- If the directory contains `.md` files, they are treated as markdown chapters.
- If the directory contains `.html` files, they are treated as HTML intake.

## Output

The build writes to the directory configured in `output.directory` (default `dist`):

- `<slug>.pdf` when `pdf = true`
- `index.html` when `html = true`

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | Build error, missing config, or missing dependency |
