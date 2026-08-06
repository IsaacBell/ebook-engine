"""Build branded PDFs from markdown chapters or HTML intake files.

Delegates markdown processing to pdf_lib; handles HTML intake directly.
Configure via ebook.toml (see BookConfig).
"""

from __future__ import annotations

import html
import shutil
import subprocess
import sys
import tempfile
import re
from pathlib import Path

from ebook_engine.config import BookConfig
from ebook_engine.css import render_pdf_css
from ebook_engine.sources.html_intake import (
    clean_html_intake,
    collect_html_files,
    extract_title,
)
from ebook_engine.sources.theme import render_theme_css, render_theme_toggle, render_analytics


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _esc(text: str) -> str:
    """HTML-escape a string for safe injection into HTML output."""
    return html.escape(text, quote=True)


def _find_weasyprint() -> str:
    """Locate the weasyprint binary, or exit with a helpful error."""
    found = shutil.which("weasyprint")
    if found:
        return found
    # macOS Homebrew fallback
    brew_path = Path("/opt/homebrew/bin/weasyprint")
    if brew_path.exists():
        return str(brew_path)
    print("Error: weasyprint not found on PATH.", file=sys.stderr)
    print("Install: brew install weasyprint  (macOS)", file=sys.stderr)
    print("         apt install weasyprint   (Debian/Ubuntu)", file=sys.stderr)
    sys.exit(1)


def _validate_output_dir(source_dir: Path, output_dir: str) -> Path:
    """Validate and resolve the output directory, rejecting path traversal."""
    resolved = (source_dir / output_dir).resolve()
    try:
        resolved.relative_to(source_dir.resolve())
    except ValueError:
        print(
            f"Error: output.directory '{output_dir}' escapes the book directory.",
            file=sys.stderr,
        )
        sys.exit(1)
    return source_dir / output_dir


def _import_pdf_lib():
    """Import pdf_lib for markdown processing. Raises a clear error if unavailable."""
    try:
        from pdf_lib.html_builder import build_html  # noqa: F401
        from pdf_lib.markdown_processor import preprocess_obsidian  # noqa: F401
    except ImportError:
        # pdf_lib is vendored into the wheel; this only triggers on a broken install.
        print(
            "Error: markdown support is missing from this installation.\n"
            "Reinstall with: pip install --force-reinstall ebook-engine",
            file=sys.stderr,
        )
        sys.exit(1)


class EbookBuild:
    """Holds config and source files for a single ebook build."""

    def __init__(self, config: BookConfig, source_dir: Path) -> None:
        self.config = config
        self.source_dir = source_dir
        self.output_dir = _validate_output_dir(source_dir, config.output_dir)
        self._book_slug = _slug(config.title)

    # ── markdown path ────────────────────────────────────────────────

    def build_markdown_html(self, files: list[Path]) -> str:
        """Build combined HTML from markdown files using pdf_lib."""
        from pdf_lib.html_builder import build_html

        return build_html(
            files,
            title=self.config.title,
            subtitle=self.config.subtitle,
            include_toc=True,
            default_author=self.config.author,
        )

    # ── HTML intake path ──────────────────────────────────────────────

    def build_html_intake(self, files: list[Path]) -> str:
        """Build combined HTML from cleaned HTML intake files."""
        parts: list[str] = []
        parts.append(
            f'<div class="cover"><h1>{_esc(self.config.title)}</h1>'
            f'<p class="cover-publisher">{_esc(self.config.subtitle)}</p></div>'
        )

        toc_entries: list[str] = []
        cleaned: list[tuple[str, str]] = []
        for i, f in enumerate(files):
            clean = clean_html_intake(f.read_text())
            title = extract_title(clean)
            anchor = f"ch{i}"
            clean = clean.replace("<h1", f'<h1 id="{anchor}"', 1)
            cleaned.append((title, clean))
            toc_entries.append(
                f'<li class="toc-h2"><a href="#{anchor}">{_esc(title)}</a></li>'
            )

        if toc_entries:
            parts.append(
                '<div class="toc-page"><h1>Contents</h1><ol class="toc-list">'
                + "\n".join(toc_entries)
                + "</ol></div>"
            )

        for _title, html_body in cleaned:
            parts.append(html_body)

        return self._wrap_pdf_html("".join(parts))

    def _wrap_pdf_html(self, body: str) -> str:
        meta = []
        if self.config.author:
            meta.append(f'<meta name="author" content="{_esc(self.config.author)}">')
        if self.config.description:
            meta.append(f'<meta name="description" content="{_esc(self.config.description)}">')
        if self.config.keywords:
            meta.append(f'<meta name="keywords" content="{_esc(self.config.keywords_str)}">')

        return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{_esc(self.config.title)}</title>
<meta name="generator" content="Ebook Engine">
{"".join(meta)}
</head>
<body>
{body}
</body>
</html>"""

    # ── PDF rendering ─────────────────────────────────────────────────

    def render_pdf(self, html_content: str) -> Path:
        weasyprint = _find_weasyprint()

        with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
            f.write(html_content)
            html_path = f.name

        with tempfile.NamedTemporaryFile(suffix=".css", mode="w", encoding="utf-8", delete=False) as f:
            # CSS string-set value: backslash-escape quotes
            css_title = self.config.title.replace('"', '\\"')
            pdf_css = render_pdf_css(accent=self.config.accent, font=self.config.font)
            css = f'body {{ string-set: book-title "{css_title}"; }}\n{pdf_css}'
            f.write(css)
            css_path = f.name

        pdf_tmp = html_path.replace(".html", ".pdf")
        out = self.output_dir / f"{self._book_slug}.pdf"

        try:
            cmd = [weasyprint, "-s", css_path, "--optimize-images",
                   "--jpeg-quality", "70", "--dpi", "150", html_path, pdf_tmp]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            for line in result.stderr.strip().splitlines():
                if any(lvl in line for lvl in ("WARNING", "ERROR", "CRITICAL")):
                    print(f"  weasyprint: {line}", file=sys.stderr)
            if result.returncode != 0:
                print(f"Error: weasyprint exited {result.returncode}", file=sys.stderr)
                sys.exit(1)

            self.output_dir.mkdir(parents=True, exist_ok=True)
            pdf_bytes = Path(pdf_tmp).read_bytes()
            if len(pdf_bytes) == 0:
                print("Error: weasyprint produced a 0-byte PDF.", file=sys.stderr)
                sys.exit(1)
            out.write_bytes(pdf_bytes)
            return out
        finally:
            for tmp in (html_path, css_path, pdf_tmp):
                try:
                    Path(tmp).unlink(missing_ok=True)
                except OSError:
                    pass

    # ── web (HTML) output ─────────────────────────────────────────────

    def build_web(self, files: list[Path]) -> Path:
        chapters: list[tuple[str, str]] = []
        for i, f in enumerate(files):
            clean = clean_html_intake(f.read_text())
            title = extract_title(clean)
            body = f'<section class="chapter" id="ch{i}">\n{clean}\n</section>'
            chapters.append((title, body))

        return self._write_web(chapters)

    def build_web_markdown(self, files: list[Path]) -> Path:
        _import_pdf_lib()
        import markdown
        from pdf_lib.markdown_processor import preprocess_obsidian

        md = markdown.Markdown(extensions=["extra", "codehilite", "toc", "sane_lists"])
        chapters: list[tuple[str, str]] = []

        for i, f in enumerate(files):
            raw = f.read_text(encoding="utf-8")
            processed = preprocess_obsidian(raw, source_file=f)
            html_body = md.convert(processed)
            md.reset()
            title_match = re.search(r"<h1>(.*?)</h1>", html_body)
            title = title_match.group(1) if title_match else f.stem.replace("-", " ").title()
            body = f'<section class="chapter" id="ch{i}">\n{html_body}\n</section>'
            chapters.append((title, body))

        return self._write_web(chapters)

    def _write_web(self, chapters: list[tuple[str, str]]) -> Path:
        toc = "\n".join(
            f'<li><a href="#ch{i}">{_esc(title)}</a></li>'
            for i, (title, _body) in enumerate(chapters)
        )
        chapter_html = "\n".join(body for _title, body in chapters)

        body = f"""\
<div class="wrapper">
<div class="cover">
<h1>{_esc(self.config.title)}</h1>
<p class="subtitle">{_esc(self.config.subtitle)}</p>
</div>
<nav class="toc"><h2>Contents</h2><ol>{toc}</ol></nav>
{chapter_html}
<footer><p>{_esc(self.config.footer)}</p></footer>
</div>"""

        meta = []
        if self.config.author:
            meta.append(f'<meta name="author" content="{_esc(self.config.author)}">')
        if self.config.description:
            meta.append(f'<meta name="description" content="{_esc(self.config.description)}">')
        if self.config.keywords:
            meta.append(f'<meta name="keywords" content="{_esc(self.config.keywords_str)}">')

        analytics_scripts = render_analytics(
            vercel=self.config.analytics_vercel,
            google_id=self.config.analytics_google,
            matomo_url=self.config.analytics_matomo_url,
            matomo_site_id=self.config.analytics_matomo_site_id,
        )

        html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_esc(self.config.title)} — {_esc(self.config.subtitle)}</title>
<meta name="generator" content="Ebook Engine">
{"".join(meta)}
<meta name="robots" content="index, follow">
{render_theme_css(self.config.accent, self.config.font)}
</head>
<body>
{render_theme_toggle()}
{body}
{analytics_scripts}
</body>
</html>"""

        self.output_dir.mkdir(parents=True, exist_ok=True)
        out = self.output_dir / "index.html"
        out.write_text(html_out, encoding="utf-8")
        return out
