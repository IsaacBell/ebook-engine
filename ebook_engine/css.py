"""Unified print stylesheet for all GridLab ebook PDFs.

Merges the best CSS from the guidebook, jj-guide, and journal builds.
The stylesheet is generated from config values (accent color, font stack)
so PDF output honors the same branding as HTML and the SVG cover.
"""

from __future__ import annotations


# GridLab brand tokens used as defaults.
_GL_INK = "#080808"
_GL_PAPER = "#F2F4F7"
_GL_CHARCOAL = "#16161A"
_GL_MATTE_BLACK = "#0D0D0D"
_GL_CYAN = "#00E5FF"


COVER_HTML = """\
<div class="cover">
<h1>{title}</h1>
<p class="cover-publisher">{subtitle}</p>
</div>
"""


def _css_escape(value: str) -> str:
    """Escape a value for safe injection into a CSS declaration context."""
    return (
        value.replace("\\", "\\\\")
        .replace("}", "\\}")
        .replace(";", "\\;")
        .replace("<", "\\3C ")
    )


def render_pdf_css(accent: str = _GL_CYAN, font: str = '"Space Mono", ui-monospace, Menlo, monospace') -> str:
    """Return the print CSS string for a given accent color and font stack."""
    accent = _css_escape(accent)
    font = _css_escape(font)
    ink = _GL_INK
    paper = _GL_PAPER
    matte = _GL_MATTE_BLACK

    return f"""
@page {{
  size: letter;
  margin: 0.75in 0.75in 0.9in 0.75in;
  @bottom-left {{
    content: string(book-title);
    font-family: {font};
    font-size: 7pt;
    color: #7c8798;
  }}
  @bottom-right {{
    content: "Page " counter(page);
    font-family: {font};
    font-size: 7pt;
    color: #7c8798;
  }}
}}

@page cover {{
  margin: 0;
  background: {matte};
  @bottom-left {{ content: none; }}
  @bottom-right {{ content: none; }}
}}

@page toc {{
  margin: 0.75in 0.75in 0.9in 0.75in;
  @bottom-left {{
    content: string(book-title);
    font-family: {font};
    font-size: 7pt;
    color: #7c8798;
  }}
  @bottom-right {{
    content: "Page " counter(page);
    font-family: {font};
    font-size: 7pt;
    color: #7c8798;
  }}
}}

html {{ font-size: 10pt; }}

body {{
  font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: {ink};
  line-height: 1.6;
  string-set: book-title "";
}}

h1, h2, h3, h4, h5, h6 {{
  font-family: {font};
  color: {ink};
}}

h1 {{
  page-break-before: always;
  font-size: 18pt;
  line-height: 1.2;
  border-bottom: 2.5pt solid {accent};
  padding-bottom: 6pt;
  margin: 0 0 14pt 0;
}}

h2 {{
  font-size: 13pt;
  margin: 16pt 0 6pt 0;
  page-break-after: avoid;
}}

h3 {{
  font-size: 11pt;
  margin: 12pt 0 4pt 0;
  page-break-after: avoid;
}}

p, li {{ font-size: 9.5pt; }}

strong {{ color: {ink}; }}

a {{ color: {accent}; }}

ul, ol {{
  margin: 0 0 8pt 0;
  padding-left: 18pt;
}}

li {{ margin-bottom: 3pt; }}

code {{
  font-family: {font};
  font-size: 8.5pt;
  background: rgba(8, 8, 8, 0.06);
  padding: 1pt 4pt;
  border-radius: 2pt;
}}

pre {{
  background: {matte};
  color: #e2e8f0;
  padding: 10pt 12pt;
  font-size: 8.5pt;
  line-height: 1.5;
  page-break-inside: avoid;
}}

pre code {{
  background: none;
  padding: 0;
  font-size: inherit;
  color: inherit;
}}

table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
  margin: 10pt 0;
}}

th {{
  font-family: {font};
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-align: left;
  color: {accent};
  border-bottom: 1.5pt solid {accent};
  padding: 4pt 6pt;
}}

td {{
  border-bottom: 0.5pt solid rgba(8, 8, 8, 0.14);
  padding: 4pt 6pt;
  vertical-align: top;
}}

tr:nth-child(even) td {{ background: rgba(0, 229, 255, 0.04); }}

blockquote {{
  border-left: 3pt solid {accent};
  margin: 10pt 0;
  padding: 4pt 12pt;
  color: #475569;
  font-style: italic;
}}

hr {{
  border: none;
  border-top: 0.5pt solid rgba(8, 8, 8, 0.15);
  margin: 16pt 0;
}}

/* Cover page */
.cover {{
  page: cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: {paper};
  text-align: center;
}}

.cover h1 {{
  font-family: {font};
  font-size: 28pt;
  color: {accent};
  border-bottom: none;
  page-break-before: auto;
  margin: 0 0 8pt 0;
}}

.cover .cover-publisher {{
  font-family: {font};
  font-size: 11pt;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin: 0 0 4pt 0;
}}

/* Table of Contents */
.toc-page {{
  page: toc;
  page-break-after: always;
}}

.toc-page h1 {{
  font-family: {font};
  font-size: 18pt;
  color: {ink};
  border-bottom: 2.5pt solid {accent};
  padding-bottom: 6pt;
  margin: 0 0 14pt 0;
  page-break-before: auto;
}}

.toc-page a {{
  color: #1e293b;
  text-decoration: none;
}}

.toc-list {{
  list-style: none;
  padding: 0;
  margin: 0;
}}

.toc-list li {{
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  margin-bottom: 4pt;
  font-size: 10pt;
  line-height: 1.6;
}}

.toc-list li a::after {{
  content: "";
}}

.toc-list li.toc-h2 {{
  font-family: {font};
  font-weight: 600;
  font-size: 10.5pt;
}}

.toc-list li.toc-h3 {{
  padding-left: 18pt;
  font-size: 9.5pt;
  color: #475569;
}}

/* Images and figures */
img {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 8pt 0;
}}

figure {{
  margin: 12pt 0;
  page-break-inside: avoid;
}}

figure img {{
  margin: 0 0 4pt 0;
}}

figcaption {{
  font-size: 8.5pt;
  color: #475569;
  font-style: italic;
  text-align: center;
}}

figcaption a {{ color: {accent}; }}
"""


# Backward-compatible alias for callers that expect the old constant.
# Prefer `render_pdf_css()` for config-driven output.
PDF_CSS = render_pdf_css()
