"""Render a terminal-style SVG "screenshot" of sample logs for each built-in theme.

Output: docs/src/assets/themes/<name>.svg  (embedded in the docs).

Run:  python tools/render_theme_svgs.py
"""

from __future__ import annotations

import html
import os

from loguru_themes import get_theme, list_themes

# (level, message) sample lines — same set the docs use.
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

FS = 15          # font size
CW = FS * 0.6    # monospace advance width
LH = 26          # line height
LEFT = 18
TITLE_H = 34
TOP = TITLE_H + 24


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def render(name: str) -> str:
    t = get_theme(name)
    bg = BG.get(name, "#1e1e1e")
    dim = t.dim
    fg = t.fg or "#cccccc"

    rows = []
    max_chars = 0
    for lvl, msg in ENTRIES:
        st = t.levels[lvl]
        badge = f"{t.icons.get(lvl)} {lvl:<8}"  # icon + space + padded name
        prefix = f"{TIME} {badge} {LOC} "
        max_chars = max(max_chars, len(prefix) + len(msg))
        rows.append((st, badge, msg, prefix))

    width = int(LEFT * 2 + max_chars * CW)
    height = int(TOP + len(ENTRIES) * LH + 12)

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="{FS}">',
        f'<rect width="{width}" height="{height}" rx="10" fill="{bg}"/>',
    ]
    # window "traffic lights"
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        p.append(f'<circle cx="{LEFT + 4 + i * 20}" cy="17" r="6" fill="{c}"/>')
    # title
    p.append(
        f'<text x="{width / 2:.0f}" y="22" fill="{dim}" font-size="13" '
        f'text-anchor="middle">{esc(name)}</text>'
    )

    for idx, (st, badge, msg, prefix) in enumerate(rows):
        y = TOP + idx * LH
        msg_x = LEFT + len(prefix) * CW
        mfg = st.msg_fg or fg
        if st.msg_bg:
            rw = (len(msg) + 1) * CW
            p.append(
                f'<rect x="{msg_x - 3:.1f}" y="{y - FS + 3:.1f}" width="{rw:.1f}" '
                f'height="{LH - 7}" rx="3" fill="{st.msg_bg}"/>'
            )
        badge_w = "700" if st.bold else "400"
        msg_w = "700" if st.msg_bold else "400"
        p.append(
            f'<text xml:space="preserve" y="{y}">'
            f'<tspan x="{LEFT}" fill="{dim}">{esc(TIME)} </tspan>'
            f'<tspan fill="{st.color}" font-weight="{badge_w}">{esc(badge)}</tspan>'
            f'<tspan fill="{dim}"> {esc(LOC)} </tspan>'
            f'<tspan fill="{mfg}" font-weight="{msg_w}">{esc(msg)}</tspan>'
            f"</text>"
        )
    p.append("</svg>")
    return "\n".join(p)


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "..", "docs", "src", "assets", "themes")
    os.makedirs(out_dir, exist_ok=True)
    for name in list_themes():
        path = os.path.join(out_dir, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(name))
        print("wrote", os.path.relpath(path, os.path.join(here, "..")))


if __name__ == "__main__":
    main()
