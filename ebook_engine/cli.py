#!/usr/bin/env python3
"""GridLab Ebook Engine — build branded PDFs or dual-theme HTML from markdown or HTML intake.

Usage:
    ebook-engine build .                    # build from ebook.toml
    ebook-engine build ./my-book/           # auto-detects source + ebook.toml
    ebook-engine init                       # create ebook.toml in current directory
"""

from __future__ import annotations

import sys
from pathlib import Path

from ebook_engine.config import BookConfig
from ebook_engine.engine import EbookBuild
from ebook_engine.sources.html_intake import collect_html_files


def _find_config(path: Path) -> Path:
    """Find ebook.toml in the given directory or its parents."""
    for parent in [path] + list(path.parents):
        candidate = parent / "ebook.toml"
        if candidate.exists():
            return candidate
    return path / "ebook.toml"


def _is_html_intake(path: Path) -> bool:
    return path.is_dir() and len(list(path.glob("*.html"))) > 0


def _collect_markdown(path: Path) -> list[Path]:
    if path.is_dir():
        files = sorted(path.rglob("*.md"))
        if not files:
            print(f"Error: no .md files found in '{path}'", file=sys.stderr)
            sys.exit(1)
        return files
    if path.suffix != ".md":
        print(f"Error: '{path}' is not a .md file", file=sys.stderr)
        sys.exit(1)
    return [path]


def cmd_init(path: Path) -> None:
    """Create an ebook.toml in the given directory."""
    target = path / "ebook.toml" if path.is_dir() else path
    if target.exists():
        print(f"Error: {target} already exists", file=sys.stderr)
        sys.exit(1)

    from ebook_engine.config import DEFAULT_CONFIG

    if target.suffix != ".toml":
        target = target / "ebook.toml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(DEFAULT_CONFIG.lstrip())
    print(f"Created {target}")


def cmd_build(path: Path) -> None:
    """Build PDF + HTML from a book directory."""
    path = path.expanduser().resolve()
    if not path.exists():
        print(f"Error: '{path}' does not exist", file=sys.stderr)
        sys.exit(1)

    config_path = _find_config(path)
    config = BookConfig.from_toml(config_path)
    build = EbookBuild(config, source_dir=path if path.is_dir() else path.parent)

    print(f"  {config.title} · {config.author}")

    if _is_html_intake(path):
        files = collect_html_files(path)
        source_type = "HTML"
        pdf_html = build.build_html_intake(files) if config.build_pdf else ""
        web_files = files
    else:
        files = _collect_markdown(path)
        source_type = "markdown"
        pdf_html = build.build_markdown_html(files) if config.build_pdf else ""
        web_files = files

    print(f"  {len(files)} {source_type} source file(s)")

    if config.build_pdf:
        pdf = build.render_pdf(pdf_html)
        size = pdf.stat().st_size / 1024
        print(f"  PDF → {pdf} ({size:.0f} KB)")

    if config.build_html:
        if _is_html_intake(path):
            web = build.build_web(web_files)
        else:
            web = build.build_web_markdown(web_files)
        size = web.stat().st_size / 1024
        print(f"  Web → {web} ({size:.0f} KB)")

    print(f"  Done — {config.output_dir}/")


def _print_usage() -> None:
    print("""\
ebook-engine — build branded PDF and dual-theme HTML from markdown or HTML files.

Usage:
  ebook-engine <command> [path]

Commands:
  init [path]       Create a new ebook.toml config file
  build [path]      Build PDF + HTML from ebook.toml (default: current directory)
  --help, -h        Show this message

Examples:
  ebook-engine init               # Create ebook.toml in current directory
  ebook-engine init my-book/      # Create ebook.toml in my-book/
  ebook-engine build              # Build from ebook.toml in current directory
  ebook-engine build my-book/     # Build from my-book/ebook.toml

Output is controlled by ebook.toml — edit it to set the title, branding, and
which formats to build (PDF, HTML, or both).

Requires Python 3.11+. PDF output requires weasyprint (brew install weasyprint).
""", file=sys.stderr)


def _parse_legacy_args(args: list[str]) -> tuple[Path, list[str]]:
    """Treat a bare path (and optional --html/--pdf flags) as a build command."""
    path = Path(args[0])
    flags = [a for a in args[1:] if a.startswith("--")]
    for flag in flags:
        if flag not in ("--html", "--pdf"):
            print(f"Unknown option: {flag}", file=sys.stderr)
            _print_usage()
            sys.exit(1)
    if flags:
        print(f"  Note: legacy flag(s) {', '.join(flags)} ignored — output is controlled by ebook.toml", file=sys.stderr)
    return path, flags


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        _print_usage()
        sys.exit(0 if len(sys.argv) < 2 else 0)

    cmd = sys.argv[1]

    if cmd == "init":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
        cmd_init(path)
    elif cmd == "build":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
        cmd_build(path)
    else:
        # Backward compatibility: `ebook-engine <path> [--html|--pdf]`
        path, _flags = _parse_legacy_args(sys.argv[1:])
        cmd_build(path)


if __name__ == "__main__":
    main()
