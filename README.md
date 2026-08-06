# Ebook Engine

[![PyPI](https://img.shields.io/pypi/v/ebook-engine.svg)](https://pypi.org/project/ebook-engine/)
[![Sponsor](https://img.shields.io/badge/Sponsor-$29_one--time-blue.svg?logo=stripe)](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09)

**Write in markdown. Build branded PDF + dual-theme HTML. One config file.**

```bash
pip install ebook-engine
ebook-engine init
ebook-engine build .
```

[Buy — $29 one-time](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09) · [Live demo](https://books-opal-alpha.vercel.app/demo)

---

## What it does

Takes a directory of markdown (or HTML) files and produces:

- **PDF** — print-ready with cover page, table of contents, running headers, syntax-highlighted code
- **HTML** — single-page web reader with light/dark theme toggle, SEO meta tags, responsive layout

Everything is configured in one `ebook.toml` file. No templating language. No YAML frontmatter required. No JavaScript framework.

## Quick start

```bash
# Install
pip install ebook-engine

# Create a new book
mkdir my-book && cd my-book
ebook-engine init

# Add some content
echo "# Chapter 1
This is the first chapter." > 01-intro.md
echo "# Chapter 2
This is the second chapter." > 02-details.md

# Build
ebook-engine build .
# → dist/my-book.pdf (PDF with cover + TOC + chapters)
# → dist/index.html (dual-theme web page)
```

## Real examples

Every format the engine produces — here's what it looks like with real content.

### Product listing → branded PDF + HTML

Source: a single HTML file describing a refurbished laptop for eBay.

```
my-listing/
├── ebook.toml     # accent = "#00E5FF", footer = "GRID[LAB]"
└── listing.html   # product description with specs, condition, shipping
```

**Output:** a dark-themed PDF suitable for attaching to invoices or printing at events, and a web page with the same content in a readable light/dark toggle. The eBay listing kit at `templates/ebay-listing.html` is a real example — inline CSS, no external dependencies, renders identically in PDF and browser.

### Technical documentation

Source: 10 HTML files exported from a writing tool — chapters on IT fundamentals (security, Linux, hardware, privacy).

```
it-guide/
├── ebook.toml
├── IT Guide - Intro to Security.html
├── IT Guide - Intro to Linux.html
├── Chapter 3_ Computer Equipment.html
└── ... (7 more files)
```

**Output:** a 1.2MB PDF with cover, TOC, and 10 properly-paginated chapters. Plus a 139KB single-page HTML site with theme toggle and Vercel Analytics. The engine automatically strips export artifacts (duplicate titles, workspace backlinks) from the HTML intake.

### Long-form ebook

Source: 10 markdown chapters on digital security and privacy — the [grid[lab] Guidebook](https://gridlab.dev).

```
guidebook/
├── ebook.toml
├── 01-mobile-security.md
├── 02-secure-communications.md
├── 03-online-privacy.md
└── ... (7 more chapters, each 1,500–2,500 words)
```

**Output:** a 3.2MB PDF with callout boxes, tables, checklists, and embedded images. The HTML version is a single-page reader with a contents sidebar and persistent theme toggle.

### Single article

Source: one markdown file — a blog post or journal article.

```
my-post/
├── ebook.toml     # build_pdf = true, build_html = true
└── post.md
```

**Output:** a 2-page PDF with metadata extracted from the article's header block (title, author, reading time, keywords). Plus an HTML page ready to deploy.

## Configuration

```toml
# ebook.toml
[book]
title = "My Book"
subtitle = "A practical guide"
author = "Jane Doe"
description = "What this book covers — used for SEO meta tags."
keywords = ["topic", "guide"]

[brand]
accent = "#00E5FF"   # GridLab Electric Cyan; used for links, headings, borders
font = '"Space Mono", ui-monospace, Menlo, monospace'
footer = "grid[lab]"  # shown at the bottom of every page

[output]
directory = "dist"
pdf = true
html = true

[analytics]
vercel = false       # inject Vercel Analytics (works on Vercel deploys)
google = ""          # Google Analytics measurement ID (e.g. "G-XXXXXXXXXX")
matomo_url = ""
matomo_site_id = ""
```

## Features

- **Dual-theme HTML** — light reader mode and dark branded mode, persisted in localStorage.
- **Configurable branding** — accent color, font stack, footer text — all in `ebook.toml`.
- **Clean HTML output** — semantic markup, proper `<title>` and `<meta>` tags, responsive at any viewport.
- **SEO-ready** — canonical URL, robots meta, description, keywords.
- **Analytics injection** — Vercel, Google Analytics, or Matomo — configured in `ebook.toml`.
- **PDF with print CSS** — running headers, page numbers, cover page, table of contents.
- **HTML intake cleaner** — strips export artifacts from Notion, Affine, and similar tools.
- **Markdown with Obsidian support** — wikilinks, image embeds, `<aside>` callouts, YAML frontmatter.
- **Safe by default** — all user values HTML-escaped, output directory validated against path traversal.
- **Capture system** — every build auto-logs to `activity/` (tee), with optional asciinema and ipynb recording.

## Not a CMS

This is a build tool, not a content management system. You write in files. You run a command. You get output artifacts. There's no database, no admin panel, no login. The source of truth is your git repo.

If you want a WYSIWYG editor with real-time collaboration, use Notion or Google Docs — then export to HTML and feed it to the engine.

## Install

```bash
pip install ebook-engine
```

Requires Python 3.11+. For PDF output, install [weasyprint](https://weasyprint.org/)
(the engine auto-detects it on PATH or at common install locations):

```bash
brew install weasyprint   # macOS
apt install weasyprint    # Debian/Ubuntu
```

## License

MIT. The source is on GitHub. The $29 purchase supports development and gives
you priority support. The engine is fully functional without a license key.

---

[Buy — $29 one-time](https://buy.stripe.com/7sY5kD0cE4x8biQ0lcfMA09) · [Live demo](https://books-opal-alpha.vercel.app/demo) · [GridLab](https://gridlab.dev)
