"""Dual-theme CSS + analytics injection for ebook HTML output.

Light = clean reader mode. Dark = branded (configurable accent).
"""

import re
import sys


def _css_escape(value: str) -> str:
    """Escape a value for safe injection into a CSS context.

    Quotes are left alone: values land in declaration position (not inside a
    CSS string), where escaping `"` would corrupt quoted font names like
    "Space Mono". Only characters that can terminate the declaration/block
    or break out of the <style> element are escaped.
    """
    return (
        value.replace("\\", "\\\\")
        .replace("}", "\\}")
        .replace(";", "\\;")
        .replace("<", "\\3C ")
    )


def render_theme_css(accent: str, font: str) -> str:
    """Return complete dual-theme CSS with configurable accent color and font stack."""
    accent = _css_escape(accent)
    font = _css_escape(font)
    try:
        accent_dim = _rgba(accent, 0.08)
        accent_dim_dark = _rgba(accent, 0.10)
    except ValueError as e:
        print(f"Error: invalid accent color '{accent}' — {e}", file=sys.stderr)
        sys.exit(1)
    return f"""<style>
:root {{
  --bg: #fafafa;
  --bg-alt: #f0f0f0;
  --bg-card: #ffffff;
  --text: #080808;
  --text-secondary: #475569;
  --accent: {accent};
  --accent-dim: {accent_dim};
  --border: #e0e0e0;
  --code-bg: #f4f4f5;
  --code-text: #080808;
  --mono: {font};
  --sans: ui-sans-serif, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --max-w: 720px;
}}

[data-theme="dark"] {{
  --bg: #16161A;
  --bg-alt: #0D0D0D;
  --bg-card: #1e1e24;
  --text: #F2F4F7;
  --text-secondary: #94a3b8;
  --accent: {accent};
  --accent-dim: {accent_dim_dark};
  --border: #2a2a30;
  --code-bg: #0D0D0D;
  --code-text: #e2e8f0;
}}

*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:17px;scroll-behavior:smooth}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.7;transition:background .2s,color .2s}}

.theme-toggle{{position:fixed;top:16px;right:16px;z-index:100;display:flex;gap:4px;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:4px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.theme-toggle button{{background:none;border:none;padding:6px 12px;border-radius:6px;font-size:13px;font-family:var(--mono);cursor:pointer;color:var(--text-secondary);transition:background .15s,color .15s}}
.theme-toggle button.active{{background:var(--accent-dim);color:var(--accent)}}

.wrapper{{max-width:var(--max-w);margin:0 auto;padding:40px 24px 80px}}

.cover{{text-align:center;padding:80px 0 60px;border-bottom:1px solid var(--border);margin-bottom:48px}}
.cover h1{{font-family:var(--mono);font-size:2.2rem;color:var(--accent);letter-spacing:-.02em;margin-bottom:8px}}
.cover .subtitle{{font-family:var(--mono);font-size:.85rem;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.12em}}

.toc{{margin-bottom:48px;padding:24px 28px;background:var(--bg-card);border:1px solid var(--border);border-radius:10px}}
.toc h2{{font-family:var(--mono);font-size:.85rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:16px}}
.toc ol{{list-style:none;counter-reset:toc}}
.toc li{{counter-increment:toc;margin-bottom:6px;font-size:.95rem}}
.toc li::before{{content:counter(toc)".";font-family:var(--mono);font-size:.8rem;color:var(--text-secondary);margin-right:10px}}
.toc a{{color:var(--text);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s}}
.toc a:hover{{border-bottom-color:var(--accent)}}

.chapter{{margin-bottom:48px;padding-top:32px;border-top:1px solid var(--border)}}
.chapter:first-of-type{{border-top:none;padding-top:0}}
.chapter h1{{font-family:var(--mono);font-size:1.5rem;color:var(--text);margin-bottom:24px;padding-bottom:12px;border-bottom:3px solid var(--accent)}}

h2{{font-family:var(--mono);font-size:1.15rem;margin:32px 0 10px;color:var(--text)}}
h3{{font-family:var(--mono);font-size:1rem;margin:24px 0 8px;color:var(--text)}}
p{{margin-bottom:14px}}
a{{color:var(--accent);text-decoration:underline;text-underline-offset:2px}}
strong{{color:var(--text)}}
ul,ol{{margin:0 0 14px 24px}}
li{{margin-bottom:6px}}

code{{font-family:var(--mono);font-size:.85rem;background:var(--code-bg);color:var(--code-text);padding:2px 6px;border-radius:3px}}
pre{{background:var(--code-bg);padding:16px 20px;border-radius:8px;overflow-x:auto;margin:16px 0;font-size:.82rem;line-height:1.55}}
pre code{{background:none;padding:0;font-size:inherit}}

blockquote{{border-left:3px solid var(--accent);margin:16px 0;padding:4px 16px;color:var(--text-secondary);font-style:italic}}

table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.9rem}}
th{{font-family:var(--mono);font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;text-align:left;color:var(--accent);border-bottom:2px solid var(--accent);padding:8px 10px}}
td{{border-bottom:1px solid var(--border);padding:8px 10px;vertical-align:top}}
tr:nth-child(even) td{{background:var(--accent-dim)}}

hr{{border:none;border-top:1px solid var(--border);margin:32px 0}}
img{{max-width:100%;height:auto;border-radius:6px;margin:12px 0}}
figure{{margin:16px 0}}
figcaption{{font-size:.8rem;color:var(--text-secondary);text-align:center;margin-top:6px}}

footer{{text-align:center;padding:40px 0 20px;border-top:1px solid var(--border);margin-top:48px;color:var(--text-secondary);font-size:.8rem;font-family:var(--mono)}}

@media(max-width:600px){{html{{font-size:15px}}.wrapper{{padding:20px 16px 60px}}.cover{{padding:48px 0 32px}}.cover h1{{font-size:1.6rem}}}}
</style>"""


def render_theme_toggle() -> str:
    """Return the theme toggle button markup with localStorage persistence."""
    return """\
<div class="theme-toggle" aria-label="Theme toggle">
  <button onclick="document.documentElement.removeAttribute('data-theme');localStorage.removeItem('theme');updateToggle()" id="btn-light" class="active">Light</button>
  <button onclick="document.documentElement.setAttribute('data-theme','dark');localStorage.setItem('theme','dark');updateToggle()" id="btn-dark">Dark</button>
</div>
<script>
(function(){
  var t=localStorage.getItem('theme');
  if(t==='dark')document.documentElement.setAttribute('data-theme','dark')
})();
function updateToggle(){
  var d=document.documentElement.getAttribute('data-theme')==='dark';
  document.getElementById('btn-light').className=d?'':'active';
  document.getElementById('btn-dark').className=d?'active':''
}
updateToggle()
</script>"""


def _js_escape(value: str) -> str:
    """Escape a value for safe injection into a double-quoted JS string."""
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("<", "\\x3c")


def render_analytics(
    vercel: bool = False,
    google_id: str = "",
    matomo_url: str = "",
    matomo_site_id: str = "",
) -> str:
    """Return analytics script tags for the configured providers."""
    scripts = []
    if vercel:
        scripts.append('<script defer src="/_vercel/insights/script.js"></script>')
    if google_id:
        gid = _js_escape(google_id)
        scripts.append(
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
            f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}'
            f'gtag("js",new Date());gtag("config","{gid}")</script>'
        )
    if matomo_url and matomo_site_id:
        mu = _js_escape(matomo_url)
        ms = _js_escape(matomo_site_id)
        scripts.append(
            f'<script>var _paq=_paq||[];_paq.push(["trackPageView"],["enableLinkTracking"]);'
            f'(function(){{var u="{mu}";'
            f'_paq.push(["setTrackerUrl",u+"matomo.php"],["setSiteId","{ms}"]);'
            f'var d=document,g=d.createElement("script"),s=d.getElementsByTagName("script")[0];'
            f'g.async=true;g.src=u+"matomo.js";s.parentNode.insertBefore(g,s)}})()</script>'
        )
    return "\n".join(scripts)


def _rgba(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba string. Raises ValueError on invalid input."""
    if not re.match(r"^#?[0-9a-fA-F]{3,8}$", hex_color):
        raise ValueError(f"expected a hex color like '#2563eb', got {hex_color!r}")
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"expected 6-digit hex, got {len(h)} digits")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
