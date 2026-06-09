"""03 — A theme is a real color scheme: native loguru tags follow the palette.

When a theme is applied, loguru's native color tags (<red>, <blue>, <RED>, …)
render in the theme's 16-color palette — like a terminal color scheme.

Run:  python examples/03_color_scheme.py
"""

import sys

from loguru import logger

from loguru_themes import apply_theme, get_theme, restore_palette, using_palette

TAGS = (
    "<red>red</red> <green>green</green> <yellow>yellow</yellow> "
    "<blue>blue</blue> <magenta>magenta</magenta> <cyan>cyan</cyan> "
    "<WHITE><black>on-white</black></WHITE>"
)


def header(text: str) -> None:
    print(f"\n=== {text} ===", file=sys.stderr, flush=True)


# Same tags, different themes -> different palettes.
for name in ("dracula", "monokai", "nord"):
    header(f"native tags in '{name}'")
    apply_theme(logger, name)
    logger.opt(colors=True).info(TAGS)

# Opt out: leave loguru's standard 16 colors alone.
header("remap_colors=False (standard ANSI)")
apply_theme(logger, "dracula", remap_colors=False)
logger.opt(colors=True).info(TAGS)

# Scope a palette to a block without applying a whole theme.
header("scoped with using_palette(nord)")
apply_theme(logger, "dracula", remap_colors=False)
with using_palette(get_theme("nord").palette):
    logger.opt(colors=True).info("inside block (Nord): " + TAGS)
logger.opt(colors=True).info("outside block (standard): " + TAGS)

restore_palette()  # tidy up the process-global state when done
