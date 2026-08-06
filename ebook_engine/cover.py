"""Generate SVG cover art representing the content pipeline v4 flow.

The cover visualizes the pipeline as a horizontal sequence of stages:
  BIN (scattered) → CARDS (linked) → OUTLINE (structured) → DRAFT → PUBLISH

Styled from the book's ebook.toml accent color and font. Zero external
dependencies — SVG is just XML.
"""

from __future__ import annotations

from typing import NamedTuple


class CoverConfig(NamedTuple):
    """Configuration for a v4 pipeline cover."""
    title: str
    subtitle: str = ""
    accent: str = "#00E5FF"        # GridLab Electric Cyan
    font: str = "Space Mono, monospace"
    width: int = 800
    height: int = 450


def _esc(text: str) -> str:
    """XML-escape text for safe SVG injection."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _lighten(hex_color: str, amount: float = 0.15) -> str:
    """Lighten a hex color by mixing with white. amount 0-1."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def _darken(hex_color: str, amount: float = 0.3) -> str:
    """Darken a hex color by reducing brightness. amount 0-1."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r * (1 - amount))
    g = int(g * (1 - amount))
    b = int(b * (1 - amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def generate(config: CoverConfig) -> str:
    """Generate a full SVG cover image as a string.

    Returns a standalone SVG document that can be saved to a .svg file
    or embedded directly in HTML.
    """
    w, h = config.width, config.height
    accent = config.accent
    light = _lighten(accent, 0.12)
    dark = _darken(accent, 0.25)
    muted = _lighten(accent, 0.25)
    bg = "#0d1117"  # dark background matching the GridLab palette

    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="accent-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{dark}"/>
      <stop offset="50%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{light}"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="url(#bg-grad)"/>

  <!-- Subtle grid -->
  <g stroke="{muted}" stroke-width="0.5" opacity="0.12">
    {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 40))}
    {"".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 40))}
  </g>

  <!-- ── Pipeline visualization ── -->

  <!-- Stage labels -->
  <g font-family="{_esc(config.font)}" font-size="10" fill="{muted}" text-anchor="middle" letter-spacing="1">
    <text x="80" y="{h - 30}">BIN</text>
    <text x="240" y="{h - 30}">CARDS</text>
    <text x="400" y="{h - 30}">OUTLINE</text>
    <text x="560" y="{h - 30}">DRAFT</text>
    <text x="720" y="{h - 30}">PUBLISH</text>
  </g>

  <!-- 1. BIN: scattered, messy, varied opacity -->
  <g fill="{accent}">
    <!-- clump of circles at different sizes -->
    <circle cx="55" cy="160" r="6" opacity="0.35"/>
    <circle cx="70" cy="150" r="4" opacity="0.5"/>
    <circle cx="85" cy="165" r="3" opacity="0.65"/>
    <circle cx="65" cy="175" r="5" opacity="0.4"/>
    <circle cx="95" cy="155" r="7" opacity="0.3"/>
    <circle cx="80" cy="140" r="3" opacity="0.55"/>
    <circle cx="50" cy="145" r="4" opacity="0.45"/>
    <circle cx="100" cy="170" r="5" opacity="0.35"/>
  </g>

  <!-- 2. CARDS: connected nodes (linked, graph-like) with edges -->
  <g>
    <!-- Edges (links between cards) -->
    <g stroke="{muted}" stroke-width="1" opacity="0.3">
      <line x1="175" y1="155" x2="200" y2="165"/>
      <line x1="200" y1="165" x2="195" y2="145"/>
      <line x1="195" y1="145" x2="215" y2="135"/>
      <line x1="195" y1="145" x2="225" y2="155"/>
      <line x1="215" y1="135" x2="240" y2="150"/>
      <line x1="225" y1="155" x2="255" y2="160"/>
      <line x1="200" y1="165" x2="225" y2="170"/>
      <line x1="240" y1="150" x2="260" y2="145"/>
      <line x1="255" y1="160" x2="280" y2="155"/>
      <line x1="225" y1="170" x2="265" y2="165"/>
    </g>
    <!-- Nodes (cards) -->
    <g fill="{accent}">
      <rect x="170" y="150" width="10" height="10" rx="2" opacity="0.6"/>
      <rect x="195" y="160" width="10" height="10" rx="2" opacity="0.7"/>
      <rect x="190" y="140" width="10" height="10" rx="2" opacity="0.55"/>
      <rect x="210" y="130" width="10" height="10" rx="2" opacity="0.75"/>
      <rect x="220" y="150" width="10" height="10" rx="2" opacity="0.65"/>
      <rect x="235" y="145" width="10" height="10" rx="2" opacity="0.5"/>
      <rect x="250" y="155" width="10" height="10" rx="2" opacity="0.6"/>
      <rect x="220" y="165" width="10" height="10" rx="2" opacity="0.45"/>
      <rect x="255" y="140" width="10" height="10" rx="2" opacity="0.7"/>
      <rect x="275" y="150" width="10" height="10" rx="2" opacity="0.55"/>
      <rect x="260" y="160" width="10" height="10" rx="2" opacity="0.5"/>
    </g>
  </g>

  <!-- Arrow: bin → cards -->
  <g stroke="{accent}" stroke-width="2" opacity="0.25">
    <line x1="115" y1="158" x2="155" y2="158"/>
    <polygon points="155,154 163,158 155,162" fill="{accent}" opacity="0.25"/>
  </g>

  <!-- 3. OUTLINE: structured, ordered blocks (human gate) -->
  <g>
    <!-- Gate line (vertical divider) -->
    <line x1="330" y1="135" x2="330" y2="180" stroke="{accent}" stroke-width="1.5" opacity="0.2" stroke-dasharray="3,3"/>
    <!-- Ordered blocks -->
    <rect x="345" y="140" width="35" height="8" rx="1.5" fill="{accent}" opacity="0.35"/>
    <rect x="345" y="152" width="35" height="8" rx="1.5" fill="{accent}" opacity="0.45"/>
    <rect x="345" y="164" width="35" height="8" rx="1.5" fill="{accent}" opacity="0.55"/>
    <!-- Position numbers -->
    <g font-family="{_esc(config.font)}" font-size="6" fill="{muted}" opacity="0.4">
      <text x="388" y="146">1</text>
      <text x="388" y="158">2</text>
      <text x="388" y="170">3</text>
    </g>
  </g>

  <!-- Arrow: cards → outline -->
  <g stroke="{accent}" stroke-width="2" opacity="0.25">
    <line x1="295" y1="158" x2="330" y2="158"/>
    <polygon points="330,154 338,158 330,162" fill="{accent}" opacity="0.25"/>
  </g>

  <!-- Arrow: outline → draft -->
  <g stroke="{accent}" stroke-width="2" opacity="0.35">
    <line x1="425" y1="158" x2="470" y2="158"/>
    <polygon points="470,154 478,158 470,162" fill="{accent}" opacity="0.35"/>
  </g>

  <!-- 4. DRAFT: clean rectangles in sequence (linear progression) -->
  <g>
    <rect x="495" y="140" width="28" height="12" rx="2" fill="{accent}" opacity="0.4"/>
    <rect x="528" y="140" width="28" height="12" rx="2" fill="{accent}" opacity="0.55"/>
    <rect x="561" y="140" width="28" height="12" rx="2" fill="{accent}" opacity="0.7"/>
    <!-- Draft text lines -->
    <g fill="{muted}" opacity="0.2">
      <rect x="495" y="158" width="28" height="2" rx="1"/>
      <rect x="528" y="158" width="28" height="2" rx="1"/>
      <rect x="561" y="158" width="28" height="2" rx="1"/>
      <rect x="495" y="163" width="20" height="2" rx="1"/>
      <rect x="528" y="163" width="22" height="2" rx="1"/>
      <rect x="561" y="163" width="18" height="2" rx="1"/>
    </g>
  </g>

  <!-- Arrow: draft → publish -->
  <g stroke="{accent}" stroke-width="2" opacity="0.45">
    <line x1="610" y1="158" x2="655" y2="158"/>
    <polygon points="655,154 663,158 655,162" fill="{accent}" opacity="0.45"/>
  </g>

  <!-- 5. PUBLISH: bold terminal rectangle + output marker -->
  <g>
    <rect x="680" y="140" width="50" height="36" rx="3" fill="none" stroke="{accent}" stroke-width="2" opacity="0.5"/>
    <!-- Checkmark inside -->
    <polyline points="692,158 700,166 716,148" fill="none" stroke="{accent}" stroke-width="2.5" opacity="0.8" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  </g>

  <!-- ── Title area ── -->
  <g text-anchor="middle">
    <text x="{w // 2}" y="85" font-family="{_esc(config.font)}" font-size="28" font-weight="700"
          fill="{accent}" letter-spacing="-0.5">{_esc(config.title)}</text>
    {f'<text x="{w // 2}" y="115" font-family="{_esc(config.font)}" font-size="14" fill="{muted}" letter-spacing="0.5">{_esc(config.subtitle)}</text>' if config.subtitle else ""}
  </g>

  <!-- ── Bottom accent line ── -->
  <rect x="0" y="{h - 4}" width="{w}" height="4" fill="url(#accent-grad)" opacity="0.6"/>

</svg>"""


def save(config: CoverConfig, path: str) -> None:
    """Generate and save an SVG cover to a file."""
    svg = generate(config)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def embed_in_html(config: CoverConfig) -> str:
    """Return the SVG as an inline HTML element for embedding in book output."""
    return generate(config)


# ── Portrait / eBook cover (2:3 aspect ratio) ──────────────────────────


class EbookCoverConfig(NamedTuple):
    """Configuration for a portrait ebook cover (2:3 ratio)."""
    title: str
    subtitle: str = ""
    author: str = ""
    accent: str = "#2563eb"
    font: str = "Space Mono, monospace"
    width: int = 600
    height: int = 900


def generate_ebook_cover(config: EbookCoverConfig) -> str:
    """Generate a portrait (2:3) ebook cover SVG.

    Layout:
      Top: Author name
      Middle: Large title + central markdown-to-book transformation icon
      Bottom: Subtitle

    Central visual: an open book rendered in glowing lines, with the left
    page showing markdown syntax characters and the right page showing clean
    formatted output. Particles flow across the spine.
    """
    w, h = config.width, config.height
    cx, cy = w // 2, h // 2
    accent = config.accent
    light = _lighten(accent, 0.1)
    dark = _darken(accent, 0.3)
    muted = _lighten(accent, 0.2)
    bg = "#0d1117"

    # ── helpers for the book visual ──
    book_top = cy - 130
    book_bottom = cy + 130
    spine_left = cx - 14
    spine_right = cx + 14
    left_page_left = cx - 150
    right_page_right = cx + 150

    return f"""\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="accent-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{dark}"/>
      <stop offset="50%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{light}"/>
    </linearGradient>
    <linearGradient id="book-glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft-glow">
      <feGaussianBlur stdDeviation="12" result="blur"/>
    </filter>
    <filter id="title-glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="url(#bg-grad)"/>

  <!-- Grid -->
  <g stroke="{muted}" stroke-width="0.5" opacity="0.10">
    {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 40))}
    {"".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 40))}
  </g>

  <!-- ── Author ── -->
  {f'''<text x="{cx}" y="85" font-family="{_esc(config.font)}" font-size="13"
        fill="{muted}" text-anchor="middle" letter-spacing="2">
    {_esc(config.author.upper())}
  </text>''' if config.author else ""}

  <!-- ── Title ── -->
  <g text-anchor="middle">
    <text x="{cx}" y="185" font-family="{_esc(config.font)}" font-size="42" font-weight="700"
          fill="{accent}" letter-spacing="-1" filter="url(#title-glow)">{_esc(config.title)}</text>
  </g>

  <!-- Accent line under title -->
  <line x1="{cx - 80}" y1="200" x2="{cx + 80}" y2="200" stroke="url(#accent-grad)" stroke-width="2" opacity="0.4"/>

  <!-- ── Central Visual: Open Book (markdown → published) ── -->

  <!-- Book background glow -->
  <ellipse cx="{cx}" cy="{cy}" rx="170" ry="150" fill="url(#book-glow)" filter="url(#soft-glow)"/>

  <!-- LEFT PAGE: markdown syntax -->
  <!-- Page shape -->
  <path d="M {left_page_left} {book_top}
           Q {left_page_left - 10} {cy} {left_page_left} {book_bottom}
           L {spine_left} {book_bottom}
           Q {spine_left + 5} {cy} {spine_left} {book_top}
           Z"
        fill="{bg}" stroke="{accent}" stroke-width="1.5" opacity="0.9"/>

  <!-- Code characters on left page (markdown syntax) -->
  <g font-family="{_esc(config.font)}" font-size="8" fill="{accent}" opacity="0.45">
    <text x="{left_page_left + 25}" y="{book_top + 30}"># heading</text>
    <text x="{left_page_left + 25}" y="{book_top + 50}">**bold text**</text>
    <text x="{left_page_left + 25}" y="{book_top + 70}">`inline code`</text>
    <text x="{left_page_left + 25}" y="{book_top + 90}">[link text](url)</text>
    <text x="{left_page_left + 25}" y="{book_top + 110}">```</text>
    <text x="{left_page_left + 25}" y="{book_top + 130}">code block</text>
    <text x="{left_page_left + 25}" y="{book_top + 150}">```</text>
    <text x="{left_page_left + 25}" y="{book_top + 175}">&gt; blockquote</text>
    <text x="{left_page_left + 25}" y="{book_top + 195}">---</text>
    <text x="{left_page_left + 25}" y="{book_top + 215}">1. ordered list</text>
  </g>

  <!-- SPINE -->
  <line x1="{spine_left}" y1="{book_top - 10}" x2="{spine_left}" y2="{book_bottom + 10}"
        stroke="{accent}" stroke-width="2" opacity="0.35"/>
  <line x1="{spine_right}" y1="{book_top - 10}" x2="{spine_right}" y2="{book_bottom + 10}"
        stroke="{accent}" stroke-width="1" opacity="0.15"/>

  <!-- RIGHT PAGE: formatted output -->
  <path d="M {spine_right} {book_top}
           Q {spine_right - 5} {cy} {spine_right} {book_bottom}
           L {right_page_right} {book_bottom}
           Q {right_page_right + 10} {cy} {right_page_right} {book_top}
           Z"
        fill="{bg}" stroke="{accent}" stroke-width="1.5" opacity="0.9"/>

  <!-- Formatted text on right page -->
  <g font-family="system-ui, sans-serif" font-size="7" fill="{light}" opacity="0.35">
    <text x="{spine_right + 20}" y="{book_top + 30}" font-weight="700" font-size="9">Heading</text>
    <text x="{spine_right + 20}" y="{book_top + 48}" font-size="6.5">This is regular paragraph text</text>
    <text x="{spine_right + 20}" y="{book_top + 62}" font-size="6.5">that flows naturally across</text>
    <text x="{spine_right + 20}" y="{book_top + 76}" font-size="6.5">the page in a clean layout.</text>
    <text x="{spine_right + 20}" y="{book_top + 95}" font-weight="700">bold text</text>
    <text x="{spine_right + 20}" y="{book_top + 113}" font-family="{_esc(config.font)}" font-size="6.5" fill="{muted}">inline code</text>
    <text x="{spine_right + 20}" y="{book_top + 133}" font-size="6.5" fill="{accent}" text-decoration="underline">link text</text>
    <text x="{spine_right + 20}" y="{book_top + 155}" font-family="{_esc(config.font)}" font-size="6" fill="{muted}">┌──────────────┐</text>
    <text x="{spine_right + 20}" y="{book_top + 168}" font-family="{_esc(config.font)}" font-size="6" fill="{muted}">│  code block   │</text>
    <text x="{spine_right + 20}" y="{book_top + 181}" font-family="{_esc(config.font)}" font-size="6" fill="{muted}">└──────────────┘</text>
    <text x="{spine_right + 20}" y="{book_top + 203}" font-size="6.5" font-style="italic">blockquote text</text>
    <text x="{spine_right + 20}" y="{book_top + 220}" font-size="6.5">1. ordered list item</text>
  </g>

  <!-- Particles flowing left → right across spine -->
  <g fill="{accent}">
    <circle cx="{left_page_left + 100}" cy="{book_top + 55}" r="1.5" opacity="0.6">
      <animate attributeName="cx" from="{left_page_left + 100}" to="{right_page_right - 80}" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="opacity" from="0.6" to="0" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{left_page_left + 90}" cy="{book_top + 105}" r="1" opacity="0.5">
      <animate attributeName="cx" from="{left_page_left + 90}" to="{right_page_right - 90}" dur="4s" repeatCount="indefinite" begin="1s"/>
      <animate attributeName="opacity" from="0.5" to="0" dur="4s" repeatCount="indefinite" begin="1s"/>
    </circle>
    <circle cx="{left_page_left + 85}" cy="{book_top + 165}" r="1.5" opacity="0.4">
      <animate attributeName="cx" from="{left_page_left + 85}" to="{right_page_right - 100}" dur="3.5s" repeatCount="indefinite" begin="2s"/>
      <animate attributeName="opacity" from="0.4" to="0" dur="3.5s" repeatCount="indefinite" begin="2s"/>
    </circle>
    <circle cx="{left_page_left + 95}" cy="{book_top + 205}" r="1" opacity="0.55">
      <animate attributeName="cx" from="{left_page_left + 95}" to="{right_page_right - 85}" dur="2.8s" repeatCount="indefinite" begin="1.5s"/>
      <animate attributeName="opacity" from="0.55" to="0" dur="2.8s" repeatCount="indefinite" begin="1.5s"/>
    </circle>
  </g>

  <!-- Particle trail dots (static) -->
  <g fill="{accent}" opacity="0.25">
    <circle cx="{spine_left - 20}" cy="{book_top + 60}" r="1"/>
    <circle cx="{spine_left - 8}" cy="{book_top + 70}" r="0.8"/>
    <circle cx="{spine_right + 8}" cy="{book_top + 90}" r="0.8"/>
    <circle cx="{spine_right + 20}" cy="{book_top + 100}" r="0.6"/>
    <circle cx="{spine_left - 15}" cy="{book_top + 170}" r="0.8"/>
    <circle cx="{spine_left - 5}" cy="{book_top + 180}" r="0.6"/>
    <circle cx="{spine_right + 12}" cy="{book_top + 195}" r="0.7"/>
    <circle cx="{spine_right + 25}" cy="{book_top + 210}" r="0.5"/>
  </g>

  <!-- ── Subtitle ── -->
  <g text-anchor="middle">
    <text x="{cx}" y="785" font-family="{_esc(config.font)}" font-size="13"
          fill="{muted}" letter-spacing="0.3">{_esc(config.subtitle)}</text>
  </g>

  <!-- ── Bottom accent line ── -->
  <rect x="0" y="{h - 4}" width="{w}" height="4" fill="url(#accent-grad)" opacity="0.5"/>

</svg>"""
