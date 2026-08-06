# Configuration

Every book is configured through `ebook.toml` in the book directory.

## Example

```toml
[book]
title = "My Book"
subtitle = "A practical guide"
author = "Jane Doe"
description = "What this book covers — used for SEO meta tags."
keywords = ["topic", "guide"]

[brand]
accent = "#00E5FF"
font = '"Space Mono", ui-monospace, Menlo, monospace'
footer = "grid[lab]"

[output]
directory = "dist"
pdf = true
html = true

[analytics]
vercel = false
google = ""
matomo_url = ""
matomo_site_id = ""
```

## Sections

### `[book]`

| Key | Description |
| --- | --- |
| `title` | Book title. Used on the cover, in the PDF title, and in HTML `<title>`. |
| `subtitle` | Subtitle shown on the cover and in the web reader header. |
| `author` | Author name. Added to PDF and HTML metadata. |
| `description` | Short description used for SEO meta tags. |
| `keywords` | List of keywords used for the HTML `<meta name="keywords">` tag. |

### `[brand]`

| Key | Description |
| --- | --- |
| `accent` | Primary color as a hex code. Used for headings, links, borders, and the theme toggle. |
| `font` | CSS font stack for headings, code, and UI elements. |
| `footer` | Text shown in the page footer of every page. |

### `[output]`

| Key | Description |
| --- | --- |
| `directory` | Output directory relative to the book directory. |
| `pdf` | Build a PDF. Requires weasyprint. |
| `html` | Build a dual-theme HTML page. |

### `[analytics]`

| Key | Description |
| --- | --- |
| `vercel` | Inject Vercel Analytics. Only works when deployed to Vercel. |
| `google` | Google Analytics measurement ID, for example `G-XXXXXXXXXX`. |
| `matomo_url` | Matomo analytics URL. |
| `matomo_site_id` | Matomo site ID. |

## Markdown features

- Obsidian-style wikilinks (`[[Another note]]`)
- Image embeds
- `<aside>` callout boxes
- YAML frontmatter
- Syntax-highlighted code blocks
