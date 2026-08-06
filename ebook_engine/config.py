"""Config loader for ebook.toml files."""

from __future__ import annotations

import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(Exception):
    """Raised when ebook.toml is missing or invalid."""
    pass


def _validate_hex_color(value: str, field_name: str) -> str:
    """Return a normalized 6-digit hex color or raise ConfigError."""
    if not isinstance(value, str):
        raise ConfigError(f"{field_name} must be a hex color string, got {type(value).__name__}")
    value = value.strip()
    if not re.match(r"^#?[0-9a-fA-F]{3,6}$", value):
        raise ConfigError(
            f"{field_name} must be a hex color like '#00E5FF', got {value!r}"
        )
    h = value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return f"#{h.upper()}"


# GridLab brand tokens used as defaults.
_GL_CYAN = "#00E5FF"
_GL_FONT = '"Space Mono", ui-monospace, Menlo, monospace'


DEFAULT_CONFIG = """\
[book]
title = "My Book"
subtitle = "A practical guide"
author = "Author Name"
description = ""
keywords = []

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
"""


@dataclass
class BookConfig:
    title: str = "My Book"
    subtitle: str = "A practical guide"
    author: str = "Author Name"
    description: str = ""
    keywords: list[str] = field(default_factory=list)

    accent: str = _GL_CYAN
    font: str = _GL_FONT
    footer: str = "grid[lab]"

    output_dir: str = "dist"
    build_pdf: bool = True
    build_html: bool = True

    analytics_vercel: bool = False
    analytics_google: str = ""
    analytics_matomo_url: str = ""
    analytics_matomo_site_id: str = ""

    @classmethod
    def from_toml(cls, path: Path) -> "BookConfig":
        if not path.exists():
            raise ConfigError(
                f"{path} not found. Run 'ebook-engine init' to create one."
            )

        with open(path, "rb") as f:
            data = tomllib.load(f)

        book = data.get("book", {})
        brand = data.get("brand", {})
        output = data.get("output", {})
        analytics = data.get("analytics", {})

        # Validate: warn on unknown keys
        KNOWN_TOP = {"book", "brand", "output", "analytics"}
        KNOWN_BOOK = {"title", "subtitle", "author", "description", "keywords"}
        KNOWN_BRAND = {"accent", "font", "footer"}
        KNOWN_OUTPUT = {"directory", "pdf", "html"}
        KNOWN_ANALYTICS = {"vercel", "google", "matomo_url", "matomo_site_id"}
        for key in data:
            if key not in KNOWN_TOP:
                print(f"  Warning: unknown section [{key}] in {path}", file=sys.stderr)
        for key in book:
            if key not in KNOWN_BOOK:
                print(f"  Warning: unknown key 'book.{key}' in {path}", file=sys.stderr)
        for key in brand:
            if key not in KNOWN_BRAND:
                print(f"  Warning: unknown key 'brand.{key}' in {path}", file=sys.stderr)
        for key in output:
            if key not in KNOWN_OUTPUT:
                print(f"  Warning: unknown key 'output.{key}' in {path}", file=sys.stderr)
        for key in analytics:
            if key not in KNOWN_ANALYTICS:
                print(f"  Warning: unknown key 'analytics.{key}' in {path}", file=sys.stderr)

        # Use a default instance for fallback values; dataclass fields with
        # default_factory are not accessible as class attributes.
        defaults = cls()

        accent = _validate_hex_color(
            brand.get("accent", defaults.accent), "brand.accent"
        )

        return cls(
            title=book.get("title", defaults.title),
            subtitle=book.get("subtitle", defaults.subtitle),
            author=book.get("author", defaults.author),
            description=book.get("description", defaults.description),
            keywords=book.get("keywords", defaults.keywords),
            accent=accent,
            font=brand.get("font", defaults.font),
            footer=brand.get("footer", defaults.footer),
            output_dir=output.get("directory", defaults.output_dir),
            build_pdf=output.get("pdf", defaults.build_pdf),
            build_html=output.get("html", defaults.build_html),
            analytics_vercel=analytics.get("vercel", defaults.analytics_vercel),
            analytics_google=analytics.get("google", defaults.analytics_google),
            analytics_matomo_url=analytics.get("matomo_url", defaults.analytics_matomo_url),
            analytics_matomo_site_id=analytics.get("matomo_site_id", defaults.analytics_matomo_site_id),
        )

    @property
    def keywords_str(self) -> str:
        return ", ".join(self.keywords) if self.keywords else ""
