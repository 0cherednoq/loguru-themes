"""Remap loguru's native color tags (``<red>``, ``<blue>``, ``<RED>`` …) to a
theme's 16-color ANSI palette.

This makes a theme behave like a real terminal color scheme: any standard
loguru color tag in a format string or a ``logger.opt(colors=True)`` message
renders in the theme's palette instead of the terminal's default 16 colors.

It works by patching loguru's internal ``AnsiParser`` color tables. The patch is
process-global (matching the "color scheme" mental model) and fully reversible
via :func:`restore_palette`.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .models import AnsiPalette

try:  # loguru internal — guard so the rest of the library works if it moves.
    from loguru._colorizer import AnsiParser as _AnsiParser
except Exception:  # pragma: no cover
    _AnsiParser = None

# palette attribute -> (loguru foreground long key, short key).
# Background keys are the upper-cased versions of these (loguru's convention).
_COLOR_KEYS = [
    ("black", "black", "k"),
    ("red", "red", "r"),
    ("green", "green", "g"),
    ("yellow", "yellow", "y"),
    ("blue", "blue", "e"),
    ("magenta", "magenta", "m"),
    ("cyan", "cyan", "c"),
    ("white", "white", "w"),
    ("bright_black", "light-black", "lk"),
    ("bright_red", "light-red", "lr"),
    ("bright_green", "light-green", "lg"),
    ("bright_yellow", "light-yellow", "ly"),
    ("bright_blue", "light-blue", "le"),
    ("bright_magenta", "light-magenta", "lm"),
    ("bright_cyan", "light-cyan", "lc"),
    ("bright_white", "light-white", "lw"),
]

# Saved originals so the patch can be undone.
_saved: "tuple[dict, dict] | None" = None


def _rgb(hex_color: str) -> "tuple[int, int, int]":
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _fg(hex_color: str) -> str:
    return "\033[38;2;%d;%d;%dm" % _rgb(hex_color)


def _bg(hex_color: str) -> str:
    return "\033[48;2;%d;%d;%dm" % _rgb(hex_color)


def palette_active() -> bool:
    """True if a theme palette is currently installed."""
    return _saved is not None


def install_palette(palette: AnsiPalette) -> None:
    """Remap loguru's named color tags to ``palette`` (process-global).

    Raises ``RuntimeError`` if loguru's internals are unavailable.
    """
    global _saved
    if _AnsiParser is None:
        raise RuntimeError(
            "cannot remap named colors: loguru internal AnsiParser is unavailable"
        )
    if _saved is None:
        _saved = (dict(_AnsiParser._foreground), dict(_AnsiParser._background))
    for attr, long, short in _COLOR_KEYS:
        hex_color = getattr(palette, attr)
        fg, bg = _fg(hex_color), _bg(hex_color)
        _AnsiParser._foreground[long] = fg
        _AnsiParser._foreground[short] = fg
        _AnsiParser._background[long.upper()] = bg
        _AnsiParser._background[short.upper()] = bg


def restore_palette() -> None:
    """Undo :func:`install_palette`, restoring loguru's default named colors."""
    global _saved
    if _saved is None or _AnsiParser is None:
        return
    fg, bg = _saved
    _AnsiParser._foreground.clear()
    _AnsiParser._foreground.update(fg)
    _AnsiParser._background.clear()
    _AnsiParser._background.update(bg)
    _saved = None


@contextmanager
def using_palette(palette: AnsiPalette) -> Iterator[None]:
    """Temporarily install a palette for the duration of a ``with`` block."""
    install_palette(palette)
    try:
        yield
    finally:
        restore_palette()
