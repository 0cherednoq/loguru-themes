"""Demo: render every log level under each built-in theme.

Run with:  python main.py
"""

from __future__ import annotations

import sys

from loguru import logger

from loguru_themes import (
    IconSet,
    apply_theme,
    build_format,
    configure_levels,
    get_theme,
    list_themes,
)

LEVELS = ("trace", "debug", "info", "success", "warning", "error", "critical")


def _emit_all_levels() -> None:
    logger.trace("entering low-level routine")
    logger.debug("resolved config from environment")
    logger.info("server listening on http://localhost:8000")
    logger.success("migration completed in 1.2s")
    logger.warning("cache miss rate above 30%")
    logger.error("failed to reach upstream service")
    logger.critical("data corruption detected — aborting")


def _header(text: str) -> None:
    # Print to the same stream loguru uses (stderr) so headers and log lines
    # stay in order — stdout and stderr are buffered separately.
    print(f"\n=== {text} ===", file=sys.stderr, flush=True)


def demo_introspect_theme(name: str = "dracula") -> None:
    """How to read a theme's icons and colors from your own code."""
    _header(f"introspecting theme: {name}")
    theme = get_theme(name)

    # Icons: theme.icons is an IconSet — attribute or .get(level).
    print("  icons:", file=sys.stderr)
    for lvl in LEVELS:
        icon = theme.icons.get(lvl)            # e.g. theme.icons.error
        print(f"    {lvl.lower():<9} {icon!r}", file=sys.stderr)

    # Colors: per-level color + the markup token, plus accent/dim/fg.
    print("  colors:", file=sys.stderr)
    for lvl in LEVELS:
        style = theme.levels[lvl.upper()]      # LevelStyle (keys are upper-case)
        print(
            f"    {lvl:<9} color={style.color}  "
            f"markup={style.markup()!r}",
            file=sys.stderr,
        )
    print(
        f"    accent={theme.accent}  dim={theme.dim}  fg={theme.fg}",
        file=sys.stderr,
    )


def demo_custom_formatter() -> None:
    """Write your OWN format string while REFERENCING the theme's colors.

    You don't hardcode hex: you read it from the theme. Two ways to use a color:
      1. `<level>...</level>` auto-uses the current record's level color (after
         configure_levels registered it) — no hex needed at all.
      2. For fixed elements, interpolate a theme color: f"<fg {theme.accent}>".
    """
    _header("your own formatter, using theme colors")
    theme = get_theme("dracula")

    logger.remove()
    # Register per-level colors + icons so <level> and {level.icon} resolve.
    configure_levels(logger, theme)

    fmt = (
        f"<fg {theme.accent}>┃</>"                       # bar in the accent color
        f" <fg {theme.dim}>{{time:HH:mm:ss}}</>"          # dim timestamp
        f" <level>{{level.icon}} {{level.name: <8}}</level>"  # per-level color (auto)
        f" <fg {theme.fg}>{{message}}</>"                 # message in the theme fg
    )
    logger.add(sys.stderr, format=fmt, colorize=True, level="TRACE")
    _emit_all_levels()

    # You can also grab a single level's markup explicitly, e.g. to color
    # something with the ERROR red:
    error_markup = theme.levels["ERROR"].markup()
    print(f"  (ERROR markup token = {error_markup!r})", file=sys.stderr)


def main() -> None:
    for name in list_themes():
        _header(f"theme: {name}")
        apply_theme(logger, name, sink=sys.stderr, colorize=True)
        _emit_all_levels()

    _header("dracula, icons disabled")
    apply_theme(logger, "dracula", icons=False, sink=sys.stderr, colorize=True)
    _emit_all_levels()

    _header("dracula, custom icon set")
    arrows = IconSet(
        trace="→", debug="→", info="→", success="✓",
        warning="▲", error="✕", critical="✕",
    )
    apply_theme(logger, "dracula", icons=arrows, sink=sys.stderr, colorize=True)
    _emit_all_levels()

    _header("dracula, customized (with_* helpers)")
    my_theme = (
        get_theme("dracula")
        .with_name("my-dracula")
        .with_color("INFO", "#ffffff")
        .with_icon("error", "!!")
        # .with_uniform_message("#e6e6e6")  # one message color for all levels
    )
    apply_theme(logger, my_theme, sink=sys.stderr, colorize=True)
    _emit_all_levels()

    _header("dracula, inline partial icon override")
    apply_theme(logger, "dracula", icons={"warning": "▲", "error": "x"},
                sink=sys.stderr, colorize=True)
    _emit_all_levels()

    # Lower-level: read a theme's icons/colors, and build your own formatter.
    demo_introspect_theme("dracula")
    demo_custom_formatter()
    demo_native_tags_use_palette()


def demo_native_tags_use_palette() -> None:
    """Native loguru tags (<red>, <blue>, …) render in the theme's palette."""
    _header("native loguru tags use the theme palette")
    apply_theme(logger, "dracula", sink=sys.stderr, colorize=True)
    line = (
        "<red>red</red> <green>green</green> <yellow>yellow</yellow> "
        "<blue>blue</blue> <magenta>magenta</magenta> <cyan>cyan</cyan>  "
        "<WHITE><black>on-white</black></WHITE>"
    )
    logger.opt(colors=True).info(line)
    print("  (same tags, theme='monokai':)", file=sys.stderr)
    apply_theme(logger, "monokai", sink=sys.stderr, colorize=True)
    logger.opt(colors=True).info(line)


if __name__ == "__main__":
    main()
