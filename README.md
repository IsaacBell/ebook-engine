# Ebook Engine

[![PyPI](https://img.shields.io/pypi/v/ebook-engine.svg)](https://pypi.org/project/ebook-engine/)

[![Turn simple text into stunning ebooks — ebook.engine](https://raw.githubusercontent.com/IsaacBell/ebook-engine/main/cover.svg)](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09)

**Write in markdown. Build a branded PDF and a dual-theme HTML page. One config file.**

```bash
uvx ebook-engine init
uvx ebook-engine build .
```

[Live demo](https://books-opal-alpha.vercel.app/demo) · [Buy — $29 one-time](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09) · [Source](https://github.com/IsaacBell/ebook-engine)

---

## What it does

Takes a directory of markdown (or HTML) files and produces:

- **PDF** — cover page, table of contents, running headers, syntax-highlighted code
- **HTML** — single-page web reader with a light/dark theme toggle, SEO meta tags, responsive layout

Everything is configured in one `ebook.toml` file. No templating language. No JavaScript framework. No frontmatter required.

## Install

Requires Python 3.11+. Pick one:

```bash
# uv (recommended) — run without installing
uvx ebook-engine --help

# uv — install as a persistent tool
uv tool install ebook-engine

# pip
pip install ebook-engine
```

For PDF output, install [weasyprint](https://weasyprint.org/) — the engine finds it on `PATH`:

```bash
brew install weasyprint   # macOS
apt install weasyprint    # Debian/Ubuntu
```

## Quick start

```bash
mkdir my-book && cd my-book
ebook-engine init

echo "# Chapter 1
This is the first chapter." > 01-intro.md

ebook-engine build .
# → dist/my-book.pdf   (cover + TOC + chapters)
# → dist/index.html    (dual-theme web page)
```

The build auto-detects the source type: `.md` files are treated as markdown chapters, `.html` files as HTML intake (exported from Notion, Affine, and similar tools — export artifacts like duplicate titles and workspace backlinks are stripped automatically).

## Configuration

`ebook-engine init` writes this `ebook.toml`:

```toml
[book]
title = "My Book"
subtitle = "A practical guide"
author = "Author Name"
description = "A description for meta tags and SEO."
keywords = ["topic", "guide"]

[brand]
accent = "#00E5FF"   # used for links, headings, borders
font = '"Space Mono", ui-monospace, Menlo, monospace'
footer = "grid[lab]" # shown at the bottom of every page

[output]
directory = "dist"
pdf = true           # requires weasyprint
html = true          # dual-theme light/dark page

[analytics]
vercel = false       # inject Vercel Analytics (works on Vercel deploys)
google = ""          # Google Analytics measurement ID (e.g. "G-XXXXXXXXXX")
matomo_url = ""
matomo_site_id = ""
```

## Features

- **Dual-theme HTML** — light reader mode and dark branded mode, persisted in localStorage
- **Configurable branding** — accent color, font stack, footer text, all in `ebook.toml`
- **SEO-ready** — canonical URL, robots meta, description, keywords
- **Analytics injection** — Vercel, Google Analytics, or Matomo
- **PDF with print CSS** — running headers, page numbers, cover page, table of contents
- **HTML intake cleaner** — strips export artifacts from Notion, Affine, and similar tools
- **Markdown with Obsidian support** — wikilinks, image embeds, callouts, YAML frontmatter
- **Safe by default** — config values are HTML-escaped; the output directory is validated against path traversal

## Not a CMS

This is a build tool, not a content management system. You write in files. You run a command. You get output artifacts. There's no database, no admin panel, no login. The source of truth is your git repo.

If you want a WYSIWYG editor with real-time collaboration, use Notion or Google Docs — then export to HTML and feed it to the engine.

## Docs

Full guides live in [`docs/`](docs/): [getting started](docs/01-getting-started.md), [configuration](docs/02-configuration.md), [CLI reference](docs/03-cli.md), [examples](docs/04-examples.md).

## License

MIT. Source: [github.com/IsaacBell/ebook-engine](https://github.com/IsaacBell/ebook-engine). The [$29 purchase](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09) supports development and gives you priority support. The engine is fully functional without a license key.
