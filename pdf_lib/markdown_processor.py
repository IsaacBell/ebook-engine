"""Obsidian-flavored markdown preprocessing."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from pdf_lib.images import resolve_obsidian_image_embeds


def _fix_malformed_citations(text: str) -> str:
    """Normalize malformed source citations like ``[[source - Text](url)]``.

    Obsidian users sometimes wrap a markdown link in wiki-link brackets.
    Convert those back to a plain markdown link so the link text and URL
    survive rendering.
    """
    # Match one or more opening brackets, then [text](url), then one or more
    # closing brackets. This catches Obsidian-style over-wrapping like
    # [[source - Text](url)] or [[[source - Text](url)]].
    pattern = re.compile(r"\[+([^\]]+)\]\(([^)]+)\)\]+")

    def repl(match: re.Match[str]) -> str:
        link_text = match.group(1).strip()
        url = match.group(2).strip()
        # Keep the link alive and wrap it in a caption-style italic.
        return f"*[{link_text}]({url})*"

    return pattern.sub(repl, text)


def _convert_wikilinks(text: str) -> str:
    """Convert Obsidian ``[[Page|alias]]`` / ``[[Page]]`` to italic text."""
    # [[Page|alias]] → *alias*
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"*\2*", text)
    # [[Page]] → *Page*
    text = re.sub(r"\[\[([^\]]+)\]\]", r"*\1*", text)
    return text


def _convert_asides(text: str) -> str:
    """Convert ``<aside>`` tags to callout divs."""
    text = re.sub(r"<aside>", '<div class="callout" markdown="1">', text)
    text = re.sub(r"</aside>", "</div>", text)
    return text


def _strip_internal_links(text: str) -> str:
    """Remove links to local files; keep external http/https/mailto links.

    PDFs cannot navigate to other local files, so ``[text](./other.md)`` or
    ``[text](04-backups)`` becomes plain ``text``. External URLs are preserved.
    Image embeds ``![alt](path)`` are left untouched.
    """

    def repl(match: re.Match[str]) -> str:
        url = match.group(2).strip()
        if "://" in url or url.startswith("mailto:"):
            return match.group(0)
        return match.group(1)

    # Negative lookbehind skips image embeds so ![alt](path) survives.
    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", repl, text)


def preprocess_obsidian(
    text: str,
    source_file: Optional[Path] = None,
    extra_assets_dirs: Optional[list[Path]] = None,
    strict_images: bool = False,
    verbose_images: bool = False,
) -> str:
    """Run the full Obsidian → standard markdown transformation.

    Order matters:
        1. Resolve image embeds first so filenames are not mangled by later steps.
        2. Fix malformed citations (before wikilink conversion eats them).
        3. Convert wikilinks to italic.
        4. Convert aside callouts.
        5. Strip internal file links.

    Args:
        text: Raw markdown text.
        source_file: File the text came from; used to resolve ``![[...]]`` image paths.
        extra_assets_dirs: Additional directories to search for images.
        strict_images: If True, raise when an image cannot be resolved.
        verbose_images: If True, print warnings for missing images.
    """
    assets_dirs = extra_assets_dirs or []

    if source_file is not None:
        text = resolve_obsidian_image_embeds(
            text,
            source_file=source_file,
            extra_assets_dirs=assets_dirs,
            strict=strict_images,
            verbose=verbose_images,
        )

    text = _fix_malformed_citations(text)
    text = _convert_wikilinks(text)
    text = _convert_asides(text)
    text = _strip_internal_links(text)
    return text
