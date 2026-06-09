"""Built-in color themes.

Palettes are drawn from each theme's canonical colors (see design D4). The
neutral ``dark`` / ``light`` themes are tuned after modern CLI tooling.

ERROR and CRITICAL additionally highlight the *message text* with a red
background (CRITICAL in bold) so failures stand out at a glance.
"""

from __future__ import annotations

from typing import Literal

from .models import LEVELS, AnsiPalette, LevelStyle, Theme

# Names of the built-in themes — used to type theme arguments so IDEs offer
# autocompletion. Keep in sync with `_PALETTES` below (a test enforces this).
ThemeName = Literal["dracula", "nord", "catppuccin", "monokai", "dark", "light"]

# Canonical 16-color terminal palettes per theme. Native loguru color tags
# (<red>, <blue>, <RED> …) are remapped to these when a theme is applied.
_ANSI_PALETTES: dict[str, AnsiPalette] = {
    "dracula": AnsiPalette(
        black="#21222c", red="#ff5555", green="#50fa7b", yellow="#f1fa8c",
        blue="#bd93f9", magenta="#ff79c6", cyan="#8be9fd", white="#f8f8f2",
        bright_black="#6272a4", bright_red="#ff6e6e", bright_green="#69ff94",
        bright_yellow="#ffffa5", bright_blue="#d6acff", bright_magenta="#ff92df",
        bright_cyan="#a4ffff", bright_white="#ffffff",
    ),
    "nord": AnsiPalette(
        black="#3b4252", red="#bf616a", green="#a3be8c", yellow="#ebcb8b",
        blue="#81a1c1", magenta="#b48ead", cyan="#88c0d0", white="#e5e9f0",
        bright_black="#4c566a", bright_red="#bf616a", bright_green="#a3be8c",
        bright_yellow="#ebcb8b", bright_blue="#81a1c1", bright_magenta="#b48ead",
        bright_cyan="#8fbcbb", bright_white="#eceff4",
    ),
    "catppuccin": AnsiPalette(
        black="#45475a", red="#f38ba8", green="#a6e3a1", yellow="#f9e2af",
        blue="#89b4fa", magenta="#f5c2e7", cyan="#94e2d5", white="#bac2de",
        bright_black="#585b70", bright_red="#f38ba8", bright_green="#a6e3a1",
        bright_yellow="#f9e2af", bright_blue="#89b4fa", bright_magenta="#f5c2e7",
        bright_cyan="#94e2d5", bright_white="#a6adc8",
    ),
    "monokai": AnsiPalette(
        black="#272822", red="#f92672", green="#a6e22e", yellow="#f4bf75",
        blue="#66d9ef", magenta="#ae81ff", cyan="#a1efe4", white="#f8f8f2",
        bright_black="#75715e", bright_red="#f92672", bright_green="#a6e22e",
        bright_yellow="#f4bf75", bright_blue="#66d9ef", bright_magenta="#ae81ff",
        bright_cyan="#a1efe4", bright_white="#f9f8f5",
    ),
    "dark": AnsiPalette(
        black="#1f2937", red="#ef4444", green="#22c55e", yellow="#f59e0b",
        blue="#38bdf8", magenta="#a78bfa", cyan="#2dd4bf", white="#e5e7eb",
        bright_black="#6b7280", bright_red="#f87171", bright_green="#4ade80",
        bright_yellow="#fbbf24", bright_blue="#60a5fa", bright_magenta="#c4b5fd",
        bright_cyan="#5eead4", bright_white="#f9fafb",
    ),
    "light": AnsiPalette(
        black="#374151", red="#dc2626", green="#16a34a", yellow="#ca8a04",
        blue="#2563eb", magenta="#9333ea", cyan="#0891b2", white="#f3f4f6",
        bright_black="#6b7280", bright_red="#ef4444", bright_green="#22c55e",
        bright_yellow="#eab308", bright_blue="#3b82f6", bright_magenta="#a855f7",
        bright_cyan="#06b6d4", bright_white="#ffffff",
    ),
}

# Per theme: level -> hex, "accent", "dim", "fg" (message foreground), and the
# message-highlight colors for error/critical ("*_msg_bg" / "*_msg_fg").
_PALETTES: dict[str, dict[str, str]] = {
    "dracula": {
        "TRACE": "#6272a4",
        "DEBUG": "#8be9fd",
        "INFO": "#bd93f9",
        "SUCCESS": "#50fa7b",
        "WARNING": "#ffb86c",
        "ERROR": "#ff5555",
        "CRITICAL": "#ff79c6",
        "accent": "#bd93f9",
        "dim": "#6272a4",
        "fg": "#f8f8f2",
        "error_msg_fg": "#ff5555",
        "critical_msg_bg": "#ff5555",
        "critical_msg_fg": "#f8f8f2",
    },
    "nord": {
        "TRACE": "#4c566a",
        "DEBUG": "#88c0d0",
        "INFO": "#81a1c1",
        "SUCCESS": "#a3be8c",
        "WARNING": "#ebcb8b",
        "ERROR": "#bf616a",
        "CRITICAL": "#b48ead",
        "accent": "#88c0d0",
        "dim": "#4c566a",
        "fg": "#e5e9f0",
        "error_msg_fg": "#bf616a",
        "critical_msg_bg": "#bf616a",
        "critical_msg_fg": "#eceff4",
    },
    "catppuccin": {
        "TRACE": "#6c7086",
        "DEBUG": "#89dceb",
        "INFO": "#cba6f7",
        "SUCCESS": "#a6e3a1",
        "WARNING": "#f9e2af",
        "ERROR": "#f38ba8",
        "CRITICAL": "#eba0ac",
        "accent": "#cba6f7",
        "dim": "#6c7086",
        "fg": "#cdd6f4",
        "error_msg_fg": "#f38ba8",
        "critical_msg_bg": "#f38ba8",
        "critical_msg_fg": "#11111b",
    },
    "monokai": {
        "TRACE": "#75715e",
        "DEBUG": "#66d9ef",
        "INFO": "#a6e22e",
        "SUCCESS": "#a6e22e",
        "WARNING": "#e6db74",
        "ERROR": "#f92672",
        "CRITICAL": "#f92672",
        "accent": "#66d9ef",
        "dim": "#75715e",
        "fg": "#f8f8f2",
        "error_msg_fg": "#f92672",
        "critical_msg_bg": "#f92672",
        "critical_msg_fg": "#f8f8f2",
    },
    "dark": {
        "TRACE": "#6b7280",
        "DEBUG": "#38bdf8",
        "INFO": "#e5e7eb",
        "SUCCESS": "#22c55e",
        "WARNING": "#f59e0b",
        "ERROR": "#ef4444",
        "CRITICAL": "#f43f5e",
        "accent": "#38bdf8",
        "dim": "#6b7280",
        "fg": "#e5e7eb",
        "error_msg_fg": "#ef4444",
        "critical_msg_bg": "#ef4444",
        "critical_msg_fg": "#f8fafc",
    },
    "light": {
        "TRACE": "#9ca3af",
        "DEBUG": "#0284c7",
        "INFO": "#1f2937",
        "SUCCESS": "#16a34a",
        "WARNING": "#b45309",
        "ERROR": "#dc2626",
        "CRITICAL": "#be123c",
        "accent": "#2563eb",
        "dim": "#9ca3af",
        "fg": "#1f2937",
        "error_msg_fg": "#dc2626",
        "critical_msg_bg": "#dc2626",
        "critical_msg_fg": "#f8fafc",
    },
}


def _build(name: str, palette: dict[str, str]) -> Theme:
    levels = {}
    for lvl in LEVELS:
        prefix = lvl.lower()
        levels[lvl] = LevelStyle(
            palette[lvl],
            bold=(lvl == "CRITICAL"),
            msg_fg=palette.get(f"{prefix}_msg_fg"),
            msg_bg=palette.get(f"{prefix}_msg_bg"),
            # CRITICAL message in bold to outrank ERROR's highlight.
            msg_bold=(lvl == "CRITICAL" and f"{prefix}_msg_bg" in palette),
        )
    return Theme(
        name=name,
        levels=levels,
        accent=palette["accent"],
        dim=palette["dim"],
        fg=palette.get("fg"),
        palette=_ANSI_PALETTES.get(name),
    )


# Name -> Theme. This dict is the immutable source of built-in defaults; the
# registry never mutates it.
BUILTIN_THEMES: dict[str, Theme] = {
    name: _build(name, palette) for name, palette in _PALETTES.items()
}
