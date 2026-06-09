"""loguru_themes — curated color themes and Unicode level icons for loguru.

Quickstart::

    from loguru import logger
    from loguru_themes import apply_theme

    apply_theme(logger, "dracula")
    logger.info("themed!")
"""

from __future__ import annotations

from .apply import apply_theme, build_format, configure_levels, resolve_icons
from .formats import make_format
from .icons import DEFAULT_ICONS, NO_ICONS
from .models import LEVELS, AnsiPalette, IconSet, LevelStyle, Theme
from .palette import (
    install_palette,
    palette_active,
    restore_palette,
    using_palette,
)
from .registry import get_theme, list_themes, register_theme
from .themes import ThemeName

__version__ = "0.1.0"

__all__ = [
    "apply_theme",
    "configure_levels",
    "build_format",
    "resolve_icons",
    "get_theme",
    "list_themes",
    "register_theme",
    "Theme",
    "ThemeName",
    "LevelStyle",
    "IconSet",
    "AnsiPalette",
    "install_palette",
    "restore_palette",
    "using_palette",
    "palette_active",
    "DEFAULT_ICONS",
    "NO_ICONS",
    "LEVELS",
    "make_format",
    "__version__",
]
