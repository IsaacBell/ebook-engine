"""Extract and normalize document metadata from markdown files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import yaml

    HAS_YAML = True
except ImportError:  # pragma: no cover - tested implicitly by import
    yaml = None  # type: ignore[assignment]
    HAS_YAML = False


@dataclass
class DocMetadata:
    """Standardized metadata for a Journal PDF."""

    title: str
    author: str = "Isaac Bell"
    description: str = ""
    keywords: str = ""
    reading_time: str = ""
    difficulty: str = ""
    subject: str = ""

    def to_meta_tags(self) -> str:
        """Return HTML <meta> tags for the document head."""
        tags = [
            f'<meta name="author" content="{self.author}">',
        ]
        if self.description:
            tags.append(f'<meta name="description" content="{self.description}">')
        if self.keywords:
            tags.append(f'<meta name="keywords" content="{self.keywords}">')
        if self.subject:
            tags.append(f'<meta name="subject" content="{self.subject}">')
        return "\n".join(tags)


def _extract_from_header_block(text: str) -> dict[str, str]:
    """Pull metadata from the GridLab chapter header block.

    Expected shape:
        # Chapter 01: Mobile Phone Security 101

        **Time to read:** 8 minutes
        **What you'll learn:** Lock screens, updates, app permissions, lost phone recovery
        **Difficulty:** Beginner
    """
    result: dict[str, str] = {}
    lines = text.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            result["title"] = stripped[2:].strip()
            # Look at the next few lines for header fields
            for j in range(i + 1, min(i + 10, len(lines))):
                field_line = lines[j].strip()
                if not field_line:
                    continue
                if field_line.startswith("**Time to read:**"):
                    result["reading_time"] = field_line.split(":", 1)[1].strip().strip("* \n\r\t")
                elif field_line.startswith("**What you'll learn:**"):
                    result["description"] = field_line.split(":", 1)[1].strip().strip("* \n\r\t")
                elif field_line.startswith("**Difficulty:**"):
                    result["difficulty"] = field_line.split(":", 1)[1].strip().strip("* \n\r\t")
            break

    return result


def _extract_keywords(text: str) -> str:
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
    return ", ".join(sorted(keywords)[:12])


def _parse_frontmatter(text: str) -> Optional[dict[str, str]]:
    """Parse YAML frontmatter if present."""
    if not HAS_YAML:
        return None
    if not text.startswith("---"):
        return None

    # Find the closing ---
    end_match = re.search(r"\n---\s*(?:\n|$)", text, re.MULTILINE)
    if not end_match:
        return None

    try:
        data = yaml.safe_load(text[3:end_match.start()])
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None

    return {str(k): str(v) if v is not None else "" for k, v in data.items()}


def extract_metadata(
    md_file: Path,
    fallback_title: Optional[str] = None,
    default_author: str = "Isaac Bell",
) -> DocMetadata:
    """Return standardized metadata for a markdown file.

    Priority:
        1. YAML frontmatter if present.
        2. Header-block extraction (GridLab chapter style).
        3. Fallback title from filename.
    """
    text = md_file.read_text(encoding="utf-8")

    frontmatter = _parse_frontmatter(text)
    header = _extract_from_header_block(text)
    filename_title = fallback_title or md_file.parent.name.replace("-", " ").title()

    title = ""
    description = ""
    reading_time = ""
    difficulty = ""

    if frontmatter:
        title = frontmatter.get("title", "")
        description = frontmatter.get("description", "")
        reading_time = frontmatter.get("reading_time", "")
        difficulty = frontmatter.get("difficulty", "")

    if not title and header.get("title"):
        title = header["title"]
    if not description and header.get("description"):
        description = header["description"]
    if not reading_time and header.get("reading_time"):
        reading_time = header["reading_time"]
    if not difficulty and header.get("difficulty"):
        difficulty = header["difficulty"]

    if not title:
        title = filename_title

    # If description came from the "What you'll learn" field, prepend a subject line.
    subject = "GridLab Journal"

    keywords = frontmatter.get("keywords", "") if frontmatter else ""
    if not keywords:
        keywords = _extract_keywords(text)

    author = default_author
    if frontmatter and frontmatter.get("author"):
        author = frontmatter["author"]

    return DocMetadata(
        title=title,
        author=author,
        description=description,
        keywords=keywords,
        reading_time=reading_time,
        difficulty=difficulty,
        subject=subject,
    )
