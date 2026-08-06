"""Clean and normalize HTML export files from writing tools (Notion, Affine, etc.).

Handles the specific patterns found in content/it-guide/ intake HTML:
  - Strips unused checkbox CSS from <head>
  - Removes duplicate filename-based <h1> (export artifact)
  - Strips affine workspace link-back nodes
  - Keeps the real chapter <h1> and all following content
"""

from __future__ import annotations

import re
from pathlib import Path
from html.parser import HTMLParser


class _Cleaner(HTMLParser):
    """Stateful parser that strips export artifacts from an HTML body.

    Removes:
      1. The first <h1> if followed by a second <h1> (duplicate title pattern).
      2. <a> links containing "workspace/" that are export back-links.
      3. Empty <div> containers added by the export tool.
    """

    def __init__(self) -> None:
        super().__init__()
        self._output: list[str] = []
        self._skip_depth: int = 0
        self._h1_count: int = 0
        self._skip_first_h1: bool = False

    def feed(self, data: str) -> None:
        # Pre-scan: skip the first <h1> if there are at least two <h1> tags.
        h1s = re.findall(r"<h1[>\s]", data)
        self._skip_first_h1 = len(h1s) >= 2
        super().feed(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._skip_depth > 0:
            self._skip_depth += 1
            return

        attr_str = _format_attrs(attrs)

        if tag == "h1" and self._h1_count == 0 and self._skip_first_h1:
            self._skip_depth = 1
            self._h1_count += 1
            return

        if tag == "h1":
            self._h1_count += 1

        # Skip workspace back-links: <a href="...workspace/...">...</a>
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v and "workspace/" in v:
                    self._skip_depth = 1
                    return

        self._output.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth > 0:
            self._skip_depth -= 1
            return
        self._output.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        self._output.append(data)

    def handle_entityref(self, name: str) -> None:
        if self._skip_depth > 0:
            return
        self._output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self._skip_depth > 0:
            return
        self._output.append(f"&#{name};")

    def get_clean_html(self) -> str:
        return "".join(self._output)


def _format_attrs(attrs: list[tuple[str, str | None]]) -> str:
    parts = []
    for k, v in attrs:
        if v is None:
            parts.append(f" {k}")
        else:
            parts.append(f' {k}="{v}"')
    return "".join(parts)


def clean_html_intake(raw: str) -> str:
    """Clean a single HTML intake file. Returns the body content only."""
    # Strip everything outside <body> (head, styles, etc.)
    body_match = re.search(r"<body>(.*)</body>", raw, re.DOTALL)
    if not body_match:
        return raw

    body = body_match.group(1)

    # Extract content from inside the wrapper div (if present)
    wrapper_match = re.search(
        r'<div style="width: 70vw; margin: 60px auto;">(.*)</div>\s*$',
        body,
        re.DOTALL,
    )
    if wrapper_match:
        body = wrapper_match.group(1)

    cleaner = _Cleaner()
    cleaner.feed(body)
    result = cleaner.get_clean_html()

    # Re-escape <script> tags that were entity-encoded in prose
    # (e.g. "&#x3C;script>" decodes to a real <script> which breaks anchors)
    result = result.replace("<script>", "&lt;script&gt;")
    result = result.replace("</script>", "&lt;/script&gt;")

    return result


def extract_title(html: str) -> str:
    """Extract the real title from cleaned HTML (the kept <h1>)."""
    match = re.search(r"<h1[>\s](.*?)</h1>", html)
    if match:
        return re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return "Untitled"


def collect_html_files(path: Path) -> list[Path]:
    """Collect .html files, excluding stubs under 1KB."""
    files: list[Path] = []
    for f in sorted(path.glob("*.html")):
        if f.stat().st_size < 1024:
            continue
        files.append(f)
    return files
