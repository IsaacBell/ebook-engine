"""Default print stylesheet for GridLab Journal PDFs."""

PDF_CSS = """
@page {
  size: letter;
  margin: 0.75in 0.75in 0.9in 0.75in;
  @bottom-left {
    content: "GridLab Journal";
    font-family: "Space Mono", ui-monospace, Menlo, monospace;
    font-size: 7pt;
    color: #7c8798;
  }
  @bottom-right {
    content: "Page " counter(page);
    font-family: "Space Mono", ui-monospace, Menlo, monospace;
    font-size: 7pt;
    color: #7c8798;
  }
}

@page cover {
  margin: 0;
  background: #0f172a;
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}

html { font-size: 10pt; }

body {
  font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1f2933;
  line-height: 1.6;
}

h1, h2, h3, h4, h5, h6 {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  color: #0f172a;
}

h1 {
  page-break-before: always;
  font-size: 18pt;
  line-height: 1.2;
  border-bottom: 2.5pt solid #38bdf8;
  padding-bottom: 6pt;
  margin: 0 0 14pt 0;
}

h2 {
  font-size: 13pt;
  margin: 16pt 0 6pt 0;
  page-break-after: avoid;
}

h3 {
  font-size: 11pt;
  margin: 12pt 0 4pt 0;
  page-break-after: avoid;
}

p, li { font-size: 9.5pt; }

strong { color: #0f172a; }

a { color: #38bdf8; }

ul, ol {
  margin: 0 0 8pt 0;
  padding-left: 18pt;
}

li { margin-bottom: 3pt; }

/* Callout boxes — converted from <aside> tags */
.callout {
  background: rgba(56, 189, 248, 0.08);
  border-left: 3pt solid #38bdf8;
  padding: 8pt 12pt;
  margin: 10pt 0;
  font-size: 9pt;
  page-break-inside: avoid;
}

.callout p:first-child { margin-top: 0; }
.callout p:last-child { margin-bottom: 0; }

code {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 8.5pt;
  background: rgba(15, 23, 42, 0.06);
  padding: 1pt 4pt;
  border-radius: 2pt;
}

pre {
  background: #0f172a;
  color: #e2e8f0;
  padding: 10pt 12pt;
  font-size: 8.5pt;
  line-height: 1.5;
  page-break-inside: avoid;
  overflow-x: auto;
}

pre code {
  background: none;
  padding: 0;
  font-size: inherit;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
  margin: 10pt 0;
}

th {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 7.5pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-align: left;
  color: #38bdf8;
  border-bottom: 1.5pt solid #38bdf8;
  padding: 4pt 6pt;
}

td {
  border-bottom: 0.5pt solid rgba(31, 41, 51, 0.14);
  padding: 4pt 6pt;
  vertical-align: top;
}

tr:nth-child(even) td { background: rgba(56, 189, 248, 0.04); }

blockquote {
  border-left: 3pt solid #38bdf8;
  margin: 10pt 0;
  padding: 4pt 12pt;
  color: #475569;
  font-style: italic;
}

hr {
  border: none;
  border-top: 0.5pt solid rgba(15, 23, 42, 0.15);
  margin: 16pt 0;
}

/* Cover page — only rendered for directory (multi-file) builds */
.cover {
  page: cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  color: #f8fafc;
  text-align: center;
}

.cover h1 {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 28pt;
  color: #38bdf8;
  border-bottom: none;
  page-break-before: auto;
  margin: 0 0 8pt 0;
}

.cover .cover-publisher {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 11pt;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin: 0 0 4pt 0;
}

.cover .cover-notes {
  font-family: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 9pt;
  color: #64748b;
  margin: 12pt 0 0 0;
  max-width: 24em;
  font-style: italic;
}

/* Table of Contents */
@page toc {
  margin: 0.75in 0.75in 0.9in 0.75in;
  @bottom-left {
    content: "GridLab Journal";
    font-family: "Space Mono", ui-monospace, Menlo, monospace;
    font-size: 7pt;
    color: #7c8798;
  }
  @bottom-right {
    content: "Page " counter(page);
    font-family: "Space Mono", ui-monospace, Menlo, monospace;
    font-size: 7pt;
    color: #7c8798;
  }
}

.toc-page {
  page: toc;
  page-break-after: always;
}

.toc-page h1 {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 18pt;
  color: #0f172a;
  border-bottom: 2.5pt solid #38bdf8;
  padding-bottom: 6pt;
  margin: 0 0 14pt 0;
  page-break-before: auto;
}

.toc-page a {
  color: #1e293b;
  text-decoration: none;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-list li {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  margin-bottom: 4pt;
  font-size: 10pt;
  line-height: 1.6;
}

.toc-list li a::after {
  content: leader('.') target-counter(attr(href), page);
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 8.5pt;
  color: #94a3b8;
}

.toc-list li.toc-h2 {
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-weight: 600;
  font-size: 10.5pt;
}

.toc-list li.toc-h3 {
  padding-left: 18pt;
  font-size: 9.5pt;
  color: #475569;
}

.toc-list li.toc-h3 a::after {
  content: leader('.') target-counter(attr(href), page);
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  font-size: 8pt;
  color: #94a3b8;
}

/* Images and figures */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 8pt 0;
}

figure {
  margin: 12pt 0;
  page-break-inside: avoid;
}

figure img {
  margin: 0 0 4pt 0;
}

figcaption {
  font-size: 8.5pt;
  color: #475569;
  font-style: italic;
  text-align: center;
}

figcaption a { color: #38bdf8; }

.missing-image {
  display: inline-block;
  border: 1pt dashed #94a3b8;
  padding: 8pt 12pt;
  color: #64748b;
  font-size: 8.5pt;
  font-family: "Space Mono", ui-monospace, Menlo, monospace;
  margin: 8pt 0;
}
"""

COVER_HTML = """\
<div class="cover">
<h1>{title}</h1>
<p class="cover-publisher">{subtitle}</p>
</div>
"""
