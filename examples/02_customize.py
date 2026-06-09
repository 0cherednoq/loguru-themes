"""02 — Tweak an existing theme with the immutable `with_*` API.

Themes are immutable: every `with_*` returns a NEW theme, so calls chain and
the original is never mutated.

Run:  python examples/02_customize.py
"""

import sys

from loguru import logger

from loguru_themes import apply_theme, get_theme


def emit() -> None:
    logger.info("info — server ready")
    logger.warning("warning — slow")
    logger.error("error — failed")
    logger.critical("critical — aborting")


def header(text: str) -> None:
    print(f"\n=== {text} ===", file=sys.stderr, flush=True)


# Chain several tweaks off a built-in theme.
header("dracula + tweaks (INFO white, ERROR icon, accent dim)")
custom = (
    get_theme("dracula")
    .with_name("my-dracula")
    .with_color("INFO", "#ffffff")        # one level's color
    .with_icon("error", "!!")             # one level's icon
    .with_dim("#7f8aa0")                  # timestamps / location color
)
apply_theme(logger, custom)
emit()

# "I like the theme but want ONE message color for everything."
header("uniform message color (no ERROR/CRITICAL highlight)")
plain = get_theme("dracula").with_uniform_message("#e6e6e6")
apply_theme(logger, plain)
emit()

# Override a single level's full style (badge + message) at once.
header("WARNING restyled (gold, bold, gold message)")
gold = get_theme("dracula").with_level(
    "WARNING", color="#ffd166", bold=True, msg_fg="#ffd166"
)
apply_theme(logger, gold)
emit()

# The original theme is untouched by any of the above.
assert get_theme("dracula").levels["INFO"].color != "#ffffff"
print("\n(original 'dracula' theme is unchanged)", file=sys.stderr)
