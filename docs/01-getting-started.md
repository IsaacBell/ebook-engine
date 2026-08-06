# Getting Started

![Ebook Engine cover](assets/cover.png)

Ebook Engine turns a folder of markdown or HTML files into a branded PDF and a dual-theme HTML page. One config file drives everything.

## Install

```bash
# uv — run without installing
uvx ebook-engine --help

# uv — install as a persistent tool
uv tool install ebook-engine

# pip
pip install ebook-engine
```

Requires Python 3.11 or newer. For PDF output you also need weasyprint:

```bash
brew install weasyprint   # macOS
apt install weasyprint    # Debian / Ubuntu
```

## Create a book

```bash
mkdir my-book && cd my-book
ebook-engine init
```

This writes an `ebook.toml` file. Add markdown chapters:

```bash
echo "# Chapter 1\n\nYour first chapter." > 01-chapter.md
echo "# Chapter 2\n\nYour second chapter." > 02-chapter.md
```

## Build

```bash
ebook-engine build .
```

Output lands in `dist/`:

- `dist/<slug>.pdf` — print-ready PDF with cover, table of contents, and running headers
- `dist/index.html` — single-page web reader with light/dark theme toggle

## HTML intake

If you already have HTML files — for example, an export from Notion, Affine, or another editor — drop them in the book folder instead of markdown. The engine cleans common export artifacts and builds the same PDF + HTML output.
