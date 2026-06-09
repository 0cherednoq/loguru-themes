"""Core data model: log levels, level styles, icon sets, and themes."""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Mapping, Union

# The seven standard loguru levels, in ascending severity.
LEVELS: tuple[str, ...] = (
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

# Sentinel for "argument not provided" where None is itself a meaningful value.
_UNSET = object()


def _normalize_level(level: str) -> str:
    upper = level.upper()
    if upper not in LEVELS:
        raise KeyError(
            f"unknown level {level!r}; valid levels: {', '.join(LEVELS)}"
        )
    return upper

_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

# Unicode Private Use Area ranges, where Nerd Font glyphs live. We forbid them
# so themes render in any terminal without a special font.
_PRIVATE_USE_RANGES = (
    (0xE000, 0xF8FF),
    (0xF0000, 0xFFFFD),
    (0x100000, 0x10FFFD),
)


def _is_private_use(char: str) -> bool:
    cp = ord(char)
    return any(lo <= cp <= hi for lo, hi in _PRIVATE_USE_RANGES)


def _validate_hex(color: str, what: str) -> None:
    if not _HEX_RE.match(color):
        raise ValueError(f"{what} must be a '#rrggbb' hex color, got {color!r}")


@dataclass(frozen=True)
class LevelStyle:
    """How a single log level is colored.

    Badge (the ``icon + LEVEL`` label):
        ``color`` — ``#rrggbb`` foreground hex; ``bold`` — bold weight;
        ``bg`` — optional badge background fill.
    Message (the log text itself):
        ``msg_fg`` / ``msg_bg`` — optional foreground / background for the
        message, e.g. a red ``msg_bg`` to highlight ERROR / CRITICAL lines;
        ``msg_bold`` — bold message text.
    """

    color: str
    bold: bool = False
    bg: "str | None" = None
    msg_fg: "str | None" = None
    msg_bg: "str | None" = None
    msg_bold: bool = False

    def __post_init__(self) -> None:
        _validate_hex(self.color, "LevelStyle.color")
        if self.bg is not None:
            _validate_hex(self.bg, "LevelStyle.bg")
        if self.msg_fg is not None:
            _validate_hex(self.msg_fg, "LevelStyle.msg_fg")
        if self.msg_bg is not None:
            _validate_hex(self.msg_bg, "LevelStyle.msg_bg")

    def markup(self) -> str:
        """Loguru color markup used as a level's ``color=`` value (the badge)."""
        parts = []
        if self.bold:
            parts.append("<bold>")
        parts.append(f"<fg {self.color}>")
        if self.bg is not None:
            parts.append(f"<bg {self.bg}>")
        return "".join(parts)

    def message_wrap(self) -> "tuple[str, str] | None":
        """Opening/closing markup for the message, or None if unstyled."""
        opens = []
        if self.msg_bold:
            opens.append("<bold>")
        if self.msg_fg is not None:
            opens.append(f"<fg {self.msg_fg}>")
        if self.msg_bg is not None:
            opens.append(f"<bg {self.msg_bg}>")
        if not opens:
            return None
        return "".join(opens), "".join("</>" for _ in opens)


@dataclass(frozen=True)
class IconSet:
    """A Unicode symbol for each standard loguru level.

    Icons must be plain Unicode (no Nerd Font / private-use glyphs) so they
    render in standard terminals without extra fonts.
    """

    trace: str
    debug: str
    info: str
    success: str
    warning: str
    error: str
    critical: str

    def __post_init__(self) -> None:
        for name in LEVELS:
            icon = getattr(self, name.lower())
            for char in icon:
                if _is_private_use(char):
                    raise ValueError(
                        f"IconSet.{name.lower()} contains a private-use "
                        f"(Nerd Font) codepoint U+{ord(char):04X}; "
                        "only standard Unicode is allowed"
                    )

    def get(self, level: str) -> str:
        """Return the icon for a level name (case-insensitive)."""
        return getattr(self, _normalize_level(level).lower())

    def replace(self, overrides: "Mapping[str, str] | None" = None, **kwargs: str) -> "IconSet":
        """Return a copy with some icons changed.

        Accepts a mapping and/or keyword level names (both case-insensitive)::

            icons.replace(error="!!", info="i")
            icons.replace({"ERROR": "!!"})
        """
        merged: dict[str, str] = {}
        for source in (overrides or {}, kwargs):
            for level, icon in source.items():
                merged[_normalize_level(level).lower()] = icon
        return replace(self, **merged)


@dataclass(frozen=True)
class AnsiPalette:
    """The 16 named ANSI colors a terminal scheme defines.

    When a theme carrying a palette is applied, loguru's native color tags
    (``<red>``, ``<blue>``, ``<RED>`` …) are remapped to these hex values — so
    a theme behaves like a real terminal color scheme, not just a few accents.
    """

    black: str
    red: str
    green: str
    yellow: str
    blue: str
    magenta: str
    cyan: str
    white: str
    bright_black: str
    bright_red: str
    bright_green: str
    bright_yellow: str
    bright_blue: str
    bright_magenta: str
    bright_cyan: str
    bright_white: str

    def __post_init__(self) -> None:
        for f in (
            "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
            "bright_black", "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
        ):
            _validate_hex(getattr(self, f), f"AnsiPalette.{f}")


@dataclass(frozen=True)
class Theme:
    """A complete color theme: per-level styles, accent/dim colors, icons.

    ``fmt`` optionally overrides the generated loguru format string; when
    ``None`` the format is built from ``dim`` at apply time (see
    :meth:`format_for`).
    """

    name: str
    levels: dict[str, LevelStyle]
    accent: str
    dim: str
    fg: "str | None" = None
    icons: "IconSet | None" = None
    fmt: "str | None" = None
    palette: "AnsiPalette | None" = None

    def __post_init__(self) -> None:
        missing = [lvl for lvl in LEVELS if lvl not in self.levels]
        if missing:
            raise ValueError(
                f"Theme {self.name!r} is missing level(s): {', '.join(missing)}"
            )
        _validate_hex(self.accent, f"Theme {self.name!r} accent")
        _validate_hex(self.dim, f"Theme {self.name!r} dim")
        if self.fg is not None:
            _validate_hex(self.fg, f"Theme {self.name!r} fg")
        if self.icons is None:
            # Lazy default to avoid an import cycle with icons.py.
            from .icons import DEFAULT_ICONS

            object.__setattr__(self, "icons", DEFAULT_ICONS)

    def format_for(self, icons: bool = True) -> str:
        """Loguru format string for this theme, with or without level icons."""
        if self.fmt is not None:
            return self.fmt
        from .formats import make_format

        return make_format(self.dim, icons=icons, fg=self.fg)

    # --- ergonomic customization -----------------------------------------
    # Theme is immutable; every helper returns a NEW theme, so calls chain:
    #
    #     my_theme = (
    #         get_theme("dracula")
    #         .with_name("my-dracula")
    #         .with_color("INFO", "#ffffff")
    #         .with_icon("error", "!!")
    #         .with_uniform_message()
    #     )

    def with_name(self, name: str) -> "Theme":
        """Return a copy with a different name (e.g. before registering)."""
        return replace(self, name=name)

    def with_accent(self, color: str) -> "Theme":
        return replace(self, accent=color)

    def with_dim(self, color: str) -> "Theme":
        return replace(self, dim=color)

    def with_fg(self, color: "str | None") -> "Theme":
        """Set the message foreground color (``None`` = terminal default)."""
        return replace(self, fg=color)

    def with_format(self, fmt: "str | None") -> "Theme":
        """Override (or clear, with ``None``) the loguru format string."""
        return replace(self, fmt=fmt)

    def with_palette(self, palette: "AnsiPalette | None") -> "Theme":
        """Set (or clear) the 16-color ANSI palette for native-tag remapping."""
        return replace(self, palette=palette)

    def with_level(self, level: str, **fields: object) -> "Theme":
        """Override one level's style fields.

        Valid fields: ``color``, ``bold``, ``bg``, ``msg_fg``, ``msg_bg``,
        ``msg_bold`` (see :class:`LevelStyle`)::

            theme.with_level("INFO", color="#ffffff", bold=True)
        """
        name = _normalize_level(level)
        new_levels = dict(self.levels)
        new_levels[name] = replace(new_levels[name], **fields)
        return replace(self, levels=new_levels)

    def with_color(self, level: str, color: str) -> "Theme":
        """Shorthand for changing a single level's badge color."""
        return self.with_level(level, color=color)

    def with_icon(self, level: str, icon: str) -> "Theme":
        """Change the icon for a single level."""
        assert self.icons is not None
        return replace(self, icons=self.icons.replace({level: icon}))

    def with_icons(self, icons: "Union[IconSet, Mapping[str, str]]") -> "Theme":
        """Replace the whole icon set, or override some icons via a mapping::

            theme.with_icons(my_icon_set)
            theme.with_icons({"error": "!!", "warning": "▲"})
        """
        if isinstance(icons, IconSet):
            return replace(self, icons=icons)
        assert self.icons is not None
        return replace(self, icons=self.icons.replace(icons))

    def with_uniform_message(self, color: object = _UNSET) -> "Theme":
        """Give every level the same plain message style.

        Clears per-level message highlighting (e.g. the red ERROR text and the
        CRITICAL background) so all messages share one color. Optionally set
        that color; otherwise the theme's current ``fg`` is kept.
        """
        new_levels = {
            name: replace(style, msg_fg=None, msg_bg=None, msg_bold=False)
            for name, style in self.levels.items()
        }
        fg = self.fg if color is _UNSET else color
        return replace(self, levels=new_levels, fg=fg)
