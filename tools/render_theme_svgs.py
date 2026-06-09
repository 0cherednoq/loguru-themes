"""Render terminal-style SVG "screenshots" for each built-in theme.

Produces, per theme, into docs/src/assets/themes/:
  <name>.svg          - sample log output (all levels)
  <name>-palette.svg  - the 16 ANSI palette colors as background swatches

Each text segment uses textLength + lengthAdjust so the layout is exact
regardless of the viewer's monospace font (keeps the CRITICAL background aligned).

Run:  python tools/render_theme_svgs.py
"""

from __future__ import annotations

import html
import os

from loguru_themes import get_theme, list_themes

ENTRIES = [
    ("TRACE", "entering low-level routine"),
    ("DEBUG", "resolved config from environment"),
    ("INFO", "server listening on http://localhost:8000"),
    ("SUCCESS", "migration completed in 1.2s"),
    ("WARNING", "cache miss rate above 30%"),
    ("ERROR", "failed to reach upstream service"),
    ("CRITICAL", "data corruption detected — aborting"),
]

# Window background per theme (the model has no explicit bg).
BG = {
    "dracula": "#282a36",
    "nord": "#2e3440",
    "catppuccin": "#1e1e2e",
    "monokai": "#272822",
    "dark": "#0d1117",
    "light": "#ffffff",
}

TIME = "10:30:00"
LOC = "app:42"

FS = 15
CW = 9.0       # grid cell width per character (text is fit to this exactly)
LH = 26
LEFT = 18
TITLE_H = 34
TOP = TITLE_H + 24

BASE = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def readable(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#11111b" if (0.299 * r + 0.587 * g + 0.114 * b) > 140 else "#f5f5f5"


def _seg(x_col: int, text: str, fill: str, weight: int) -> str:
    """A text segment fit to exactly len(text) grid cells starting at x_col."""
    return (
        f'<text x="{LEFT + x_col * CW:.1f}" y="{{y}}" fill="{fill}" '
        f'font-weight="{weight}" textLength="{len(text) * CW:.1f}" '
        f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(text)}</text>'
    )


def _window_open(width: int, height: int, name: str, dim: str, bg: str) -> list[str]:
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="{FS}">',
        f'<rect width="{width}" height="{height}" rx="10" fill="{bg}"/>',
    ]
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        p.append(f'<circle cx="{LEFT + 4 + i * 20}" cy="17" r="6" fill="{c}"/>')
    p.append(
        f'<text x="{width / 2:.0f}" y="22" fill="{dim}" font-size="13" '
        f'text-anchor="middle">{esc(name)}</text>'
    )
    return p


def render_log(name: str) -> str:
    t = get_theme(name)
    bg = BG.get(name, "#1e1e1e")
    dim, fg = t.dim, (t.fg or "#cccccc")

    badge_col = len(TIME) + 1            # after "time "
    loc_col = badge_col + 10 + 1         # after "time badge "
    msg_col = loc_col + len(LOC) + 1     # after "time badge loc "
    max_chars = msg_col + max(len(m) for _, m in ENTRIES)

    width = int(LEFT * 2 + max_chars * CW)
    height = int(TOP + len(ENTRIES) * LH + 12)
    p = _window_open(width, height, name, dim, bg)

    for idx, (lvl, msg) in enumerate(ENTRIES):
        st = t.levels[lvl]
        y = TOP + idx * LH
        if st.msg_bg:
            x = LEFT + msg_col * CW
            p.append(
                f'<rect x="{x - 3:.1f}" y="{y - FS + 3:.1f}" '
                f'width="{len(msg) * CW + 6:.1f}" height="{LH - 7}" rx="3" '
                f'fill="{st.msg_bg}"/>'
            )
        badge = f"{t.icons.get(lvl)} {lvl:<8}"
        segs = [
            _seg(0, TIME, dim, 400),
            _seg(badge_col, badge, st.color, 700 if st.bold else 400),
            _seg(loc_col, LOC, dim, 400),
            _seg(msg_col, msg, st.msg_fg or fg, 700 if st.msg_bold else 400),
        ]
        for s in segs:
            p.append(s.replace("{y}", str(y)))
    p.append("</svg>")
    return "\n".join(p)


def render_palette(name: str) -> str:
    t = get_theme(name)
    pal = t.palette
    bg = BG.get(name, "#1e1e1e")
    dim = t.dim

    cell_w, cell_h, gap = 104, 38, 8
    cols = 8
    top = TITLE_H + 12
    width = int(LEFT * 2 + cols * cell_w + (cols - 1) * gap)
    height = int(top + 2 * (cell_h + gap) + 4)
    p = _window_open(width, height, f"{name} · palette", dim, bg)

    rows = [("", BASE), ("+", ["bright_" + c for c in BASE])]
    for r, (prefix, names) in enumerate(rows):
        y = top + r * (cell_h + gap)
        for i, cname in enumerate(names):
            hexv = getattr(pal, cname)
            x = LEFT + i * (cell_w + gap)
            label = prefix + cname.replace("bright_", "")
            p.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="5" fill="{hexv}"/>')
            p.append(
                f'<text x="{x + cell_w / 2:.0f}" y="{y + cell_h / 2 + 4:.0f}" '
                f'fill="{readable(hexv)}" font-size="12" text-anchor="middle">{esc(label)}</text>'
            )
    p.append("</svg>")
    return "\n".join(p)


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "..", "docs", "src", "assets", "themes")
    os.makedirs(out_dir, exist_ok=True)
    for name in list_themes():
        for suffix, svg in ((f"{name}", render_log(name)), (f"{name}-palette", render_palette(name))):
            path = os.path.join(out_dir, f"{suffix}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print("wrote", os.path.relpath(path, os.path.join(here, "..")))


if __name__ == "__main__":
    main()
