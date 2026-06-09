"""Applying themes to loguru loggers.

`apply_theme` is the one-call entry point. For finer control, the building
blocks it is composed of are public too:

- `configure_levels(logger, theme)` registers per-level colors + icons on a
  logger (via ``logger.level(...)``) without adding any sink — wire your own
  ``logger.add(...)`` afterwards.
- `build_format(theme)` returns the loguru ``format`` value (a string, or a
  callable for themes with per-level message highlighting) to pass to your own
  ``logger.add(...)``.
"""

from __future__ import annotations

import sys
import warnings
from collections.abc import Mapping
from typing import Any, Optional, Union

from .formats import make_format
from .icons import NO_ICONS
from .models import LEVELS, IconSet, Theme
from .palette import install_palette, restore_palette
from .registry import get_theme
from .themes import ThemeName

IconsSpec = Union[bool, IconSet, Mapping[str, str]]
# A theme argument: a built-in name (autocompleted), any registered name, or a Theme.
ThemeLike = Union[ThemeName, str, Theme]

# id(logger) -> handler id added by this library, so re-applying replaces our
# own sink instead of stacking duplicates.
_MANAGED: dict[int, int] = {}


def _resolve_theme(theme: ThemeLike) -> Theme:
    resolved = get_theme(theme) if isinstance(theme, str) else theme
    if not isinstance(resolved, Theme):
        raise TypeError(f"theme must be a name or Theme, got {type(theme).__name__}")
    return resolved


def resolve_icons(theme: Theme, icons: IconsSpec) -> "tuple[IconSet, bool]":
    """Resolve an ``icons`` spec to a concrete ``(IconSet, enabled)`` pair.

    ``True`` -> the theme's icons; ``False`` -> blanked icons (disabled); an
    :class:`IconSet` -> used as-is; a mapping -> the theme's icons with those
    levels overridden.
    """
    assert theme.icons is not None
    if isinstance(icons, IconSet):
        return icons, True
    if isinstance(icons, Mapping):
        return theme.icons.replace(icons), True
    if icons:
        return theme.icons, True
    return NO_ICONS, False


def configure_levels(
    logger: Any,
    theme: ThemeLike,
    *,
    icons: IconsSpec = True,
) -> Theme:
    """Register the theme's per-level color and icon on ``logger``.

    Calls ``logger.level(name, color=..., icon=...)`` for every standard level
    and adds **no sink** — so you keep full control of your own
    ``logger.add(...)`` (format, sinks, rotation, etc.). Use ``<level>`` and
    ``{level.icon}`` in your format string to pick up the colors and icons.

    Returns the resolved :class:`Theme` (handy for a following
    :func:`build_format`).
    """
    resolved = _resolve_theme(theme)
    icon_set, _ = resolve_icons(resolved, icons)
    for name in LEVELS:
        style = resolved.levels[name]
        logger.level(name, color=style.markup(), icon=icon_set.get(name))
    return resolved


def build_format(theme: ThemeLike, *, icons: IconsSpec = True):
    """Return the loguru ``format`` value for ``theme``.

    Returns a plain format string, or — for themes with per-level message
    highlighting (e.g. red ERROR text) — a callable formatter. Either can be
    passed straight to ``logger.add(sink, format=build_format(theme), ...)``.
    A custom ``theme.fmt`` is returned verbatim.
    """
    resolved = _resolve_theme(theme)
    _, icons_enabled = resolve_icons(resolved, icons)

    if resolved.fmt is not None:
        return resolved.fmt

    has_message_styles = any(
        style.message_wrap() is not None for style in resolved.levels.values()
    )
    if not has_message_styles:
        return resolved.format_for(icons_enabled)

    default_message = (
        f"<fg {resolved.fg}>{{message}}</>" if resolved.fg else "{message}"
    )

    def _formatter(record) -> str:
        style = resolved.levels.get(record["level"].name)
        wrap = style.message_wrap() if style is not None else None
        if wrap is not None:
            opens, closes = wrap
            message = f"{opens}{{message}}{closes}"
        else:
            message = default_message
        # A callable format must add the newline and exception itself.
        return (
            make_format(resolved.dim, icons=icons_enabled, message=message)
            + "\n{exception}"
        )

    return _formatter


def apply_theme(
    logger: Any,
    theme: ThemeLike,
    *,
    icons: IconsSpec = True,
    sink: Any = None,
    level: str = "TRACE",
    colorize: Optional[bool] = None,
    replace: bool = True,
    remap_colors: bool = True,
) -> int:
    """Configure ``logger`` to render with ``theme``'s colors, format, and icons.

    Parameters
    ----------
    logger:
        A loguru logger (e.g. ``from loguru import logger``).
    theme:
        A theme name (case-insensitive) or a :class:`Theme` instance.
    icons:
        ``True`` for the theme's icons, ``False`` to disable icons, a custom
        :class:`IconSet` to replace them, or a mapping like
        ``{"error": "!!"}`` to override just some levels.
    sink:
        Output sink; defaults to ``sys.stderr``.
    level:
        Minimum level for the sink.
    colorize:
        Force color on/off. ``None`` (default) lets loguru auto-detect, so output
        degrades to plain text on non-color streams.
    replace:
        When True (default) take over the logger by removing all existing
        handlers first — the idiomatic loguru "configure the console" pattern.
        When False, only the handler previously added by this library is removed.
    remap_colors:
        When True (default), remap loguru's native color tags (``<red>``,
        ``<blue>``, ``<RED>`` …) to the theme's 16-color palette, so the theme
        acts as a full color scheme. This is process-global; pass False to leave
        loguru's standard colors untouched. Themes without a palette restore the
        defaults. Undo manually with ``restore_palette()``.

    Returns the loguru handler id of the installed sink.

    For more control, compose the building blocks yourself::

        configure_levels(logger, "dracula")          # colors + icons
        logger.add(sys.stderr, format=build_format("dracula"))
    """
    resolved = _resolve_theme(theme)
    key = id(logger)

    if replace:
        logger.remove()
        _MANAGED.pop(key, None)
    else:
        prev = _MANAGED.get(key)
        if prev is not None:
            try:
                logger.remove(prev)
            except ValueError:
                pass  # already removed elsewhere
            _MANAGED.pop(key, None)

    if remap_colors:
        if resolved.palette is not None:
            try:
                install_palette(resolved.palette)
            except RuntimeError as exc:  # loguru internals unavailable
                warnings.warn(f"named-color remapping skipped: {exc}", stacklevel=2)
        else:
            restore_palette()

    configure_levels(logger, resolved, icons=icons)
    fmt = build_format(resolved, icons=icons)
    target = sys.stderr if sink is None else sink

    handler_id = logger.add(target, format=fmt, colorize=colorize, level=level)
    _MANAGED[key] = handler_id
    return handler_id
