"""Resolve Obsidian image embeds into weasyprint-friendly HTML/markdown."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from html import escape as html_escape

import markdown


def _image_search_dirs(source_file: Path, extra_assets_dirs: list[Path]) -> list[Path]:
    """Return ordered list of directories to search for an image.

    Order:
        1. Directory containing the source markdown file.
        2. Sibling ``assets/images/`` directory.
        3. Sibling ``assets/`` directory.
        4. Parent directories, up to the repository root (where ``.git`` lives)
           or the filesystem root.
        5. Any user-supplied ``--assets-dir`` paths.
    """
    dirs: list[Path] = [source_file.parent]

    assets_images = source_file.parent / "assets" / "images"
    if assets_images.is_dir():
        dirs.append(assets_images)

    assets = source_file.parent / "assets"
    if assets.is_dir():
        dirs.append(assets)

    # Walk upward so Obsidian vault attachments at the repo root are found.
    current = source_file.parent.resolve()
    while True:
        parent = current.parent
        if parent == current:
            break
        if parent not in dirs:
            dirs.append(parent)
        if (parent / ".git").is_dir():
            break
        current = parent

    for d in extra_assets_dirs:
        resolved = d.expanduser().resolve()
        if resolved.is_dir() and resolved not in dirs:
            dirs.append(resolved)

    return dirs


def _resolve_image(filename: str, source_file: Path, extra_assets_dirs: list[Path]) -> Path | None:
    """Find an image file on disk or return None."""
    for directory in _image_search_dirs(source_file, extra_assets_dirs):
        candidate = directory / filename
        if candidate.is_file():
            return candidate.resolve()
    return None


def _file_url(path: Path) -> str:
    """Return a file:// URL that weasyprint can resolve reliably."""
    # Resolve symlinks (e.g. /tmp on macOS) and quote parts for spaces/special chars.
    resolved = path.resolve()
    parts = [quote(part, safe="") for part in resolved.parts]
    if resolved.is_absolute() and parts and parts[0] == "%2F":
        parts[0] = ""
    joined = "/".join(parts)
    if resolved.is_absolute():
        return "file://" + joined
    return "file:" + joined


def _missing_image_html(filename: str) -> str:
    """Render a visible placeholder for a missing image."""
    return (
        f'<span class="missing-image">Image not found: {html_escape(filename)}</span>'
    )


def _caption_to_html(caption: str) -> str:
    """Render a caption that may contain markdown links as HTML."""
    # Use a minimal Markdown converter for the caption only.
    md = markdown.Markdown(extensions=[])
    html = md.convert(caption)
    # markdown wraps simple text in <p>; strip the wrapper for figcaption.
    html = html.strip()
    if html.startswith("<p>") and html.endswith("</p>"):
        html = html[3:-4].strip()
    return html


IMAGE_EMBED_RE = re.compile(r"!\[\[(.*?)\]\]")


def resolve_obsidian_image_embeds(
    text: str,
    source_file: Path,
    extra_assets_dirs: list[Path],
    strict: bool = False,
    verbose: bool = False,
) -> str:
    """Convert Obsidian ``![[filename]]`` and ``![[filename|caption]]`` embeds.

    Uncaptioned embeds become standard markdown images. Captioned embeds become
    ``<figure>`` blocks so the caption survives PDF rendering intact.
    """

    def repl(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        if "|" in inner:
            filename, caption = inner.split("|", 1)
        else:
            filename = inner
            caption = ""

        filename = filename.strip()
        caption = caption.strip()

        resolved = _resolve_image(filename, source_file, extra_assets_dirs)

        if resolved is None:
            message = f"Image not found: {filename}"
            if strict:
                raise FileNotFoundError(message)
            if verbose:
                print(f"  warning: {message}", flush=True)
            return _missing_image_html(filename)

        src = _file_url(resolved)

        if caption:
            caption_html = _caption_to_html(caption)
            return (
                f"\n<figure>\n"
                f'  <img src="{src}" alt="{html_escape(filename)}">\n'
                f"  <figcaption>{caption_html}</figcaption>\n"
                f"</figure>\n"
            )

        return f"![{filename}]({src})"

    return IMAGE_EMBED_RE.sub(repl, text)
