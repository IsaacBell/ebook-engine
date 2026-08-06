"""Assemble pre-processed markdown into a complete HTML document."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

import markdown

from pdf_lib.css import COVER_HTML
from pdf_lib.metadata import extract_metadata


def _collect_keywords(text: str) -> set[str]:
    """Collect keywords from H2/H3 headings."""
    keywords: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            kw = stripped[3:].strip()
            if len(kw) > 2:
                keywords.add(kw)
        elif stripped.startswith("### "):
            kw = stripped[4:].strip()
            if len(kw) > 2:
                keywords.add(kw)
    return keywords


class _HeadingCollector(HTMLParser):
    """Extract heading text + id from rendered HTML for the TOC."""

    def __init__(self) -> None:
        super().__init__()
        self.entries: list[tuple[str, str, str]] = []  # (id, text, level)
        self._current_tag: str | None = None
        self._current_id: str | None = None
        self._current_text: list[str] = []
        self._depth: int = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("h2", "h3"):
            self._current_tag = tag
            self._current_text = []
            for k, v in attrs:
                if k == "id" and v:
                    self._current_id = v
                    break
            self._depth += 1
        elif self._current_tag:
            self._depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self._current_tag:
            self._depth -= 1
        if tag == self._current_tag and self._depth == 0:
            if self._current_id:
                text = "".join(self._current_text).strip()
                level = "toc-h2" if tag == "h2" else "toc-h3"
                self.entries.append((self._current_id, text, level))
            self._current_tag = None
            self._current_id = None

    def handle_data(self, data: str) -> None:
        if self._current_tag:
            self._current_text.append(data)


def _build_toc(rendered_html: list[str]) -> str:
    """Build an HTML TOC from already-rendered file HTML."""
    entries: list[str] = []
    seen: set[str] = set()

    for html in rendered_html:
        collector = _HeadingCollector()
        collector.feed(html)

        for anchor_id, heading, css_class in collector.entries:
            if anchor_id in seen:
                continue
            seen.add(anchor_id)
            entries.append(
                '<li class="' + css_class + '"><a href="#' + anchor_id + '">'
                + heading + "</a></li>"
            )

    if not entries:
        return ""

    return (
        '<div class="toc-page">\n'
        '<h1>Contents</h1>\n'
        '<ol class="toc-list">\n'
        + "".join(entries)
        + "\n</ol>\n</div>"
    )


def build_html(
    files: list[Path],
    title: str | None = None,
    subtitle: str | None = None,
    include_toc: bool = True,
    default_author: str = "Isaac Bell",
    extra_assets_dirs: list[Path] | None = None,
    strict_images: bool = False,
    verbose_images: bool = False,
) -> str:
    """Convert collected markdown files to a single HTML document."""
    from pdf_lib.markdown_processor import preprocess_obsidian

    assets_dirs = extra_assets_dirs or []

    md = markdown.Markdown(extensions=["extra", "codehilite", "toc", "sane_lists"])

    metadata = extract_metadata(files[0], fallback_title=title, default_author=default_author)
    doc_title = title if title else metadata.title
    doc_subtitle = subtitle if subtitle else "GridLab"

    # Pre-process and render each file once. We reuse the rendered HTML for
    # both the TOC and the body so image warnings are emitted exactly once.
    rendered: list[str] = []
    heading_keywords: set[str] = set()

    for f in files:
        raw_text = f.read_text(encoding="utf-8")
        heading_keywords |= _collect_keywords(raw_text)
        processed_text = preprocess_obsidian(
            raw_text,
            source_file=f,
            extra_assets_dirs=assets_dirs,
            strict_images=strict_images,
            verbose_images=verbose_images,
        )
        rendered.append(md.convert(processed_text))
        md.reset()

    # Merge with metadata keywords, preserving metadata order then appending extras
    existing_keywords = [k.strip() for k in metadata.keywords.split(",") if k.strip()]
    merged: list[str] = []
    seen: set[str] = set()
    for kw in existing_keywords + sorted(heading_keywords):
        lower = kw.lower()
        if lower not in seen:
            seen.add(lower)
            merged.append(kw)
    metadata.keywords = ", ".join(merged[:24])

    parts: list[str] = []

    # Cover page only for directory (multi-file) builds
    if len(files) > 1:
        parts.append(COVER_HTML.format(title=doc_title, subtitle=doc_subtitle))

    if include_toc:
        toc_html = _build_toc(rendered)
        if toc_html:
            parts.append(toc_html)

    parts.extend(rendered)

    meta_tags = metadata.to_meta_tags()

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{doc_title}</title>
<meta name="generator" content="GridLab Journal">
{meta_tags}
</head>
<body>
{ "".join(parts) }
</body>
</html>"""
