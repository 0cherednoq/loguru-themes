"""Theme registry: look up, list, and register themes by name."""

from __future__ import annotations

from typing import Union

from .models import Theme
from .themes import BUILTIN_THEMES, ThemeName

# Custom themes registered at runtime. Kept separate from BUILTIN_THEMES so the
# built-in defaults can never be corrupted.
_CUSTOM_THEMES: dict[str, Theme] = {}


def _all() -> dict[str, Theme]:
    merged = dict(BUILTIN_THEMES)
    merged.update(_CUSTOM_THEMES)
    return merged


def list_themes() -> list[str]:
    """Return all available theme names (built-in + registered), sorted."""
    return sorted(_all())


def get_theme(name: Union[ThemeName, str]) -> Theme:
    """Look up a theme by name, case-insensitively.

    Raises ``KeyError`` listing available names if not found.
    """
    if not isinstance(name, str):
        raise TypeError(f"theme name must be a string, got {type(name).__name__}")
    key = name.lower()
    for tname, theme in _all().items():
        if tname.lower() == key:
            return theme
    available = ", ".join(list_themes())
    raise KeyError(f"unknown theme {name!r}; available: {available}")


def register_theme(theme: Theme, *, overwrite: bool = False) -> None:
    """Register a custom theme so it can be looked up / applied by name.

    Raises ``ValueError`` if the name already exists and ``overwrite`` is False.
    Built-in theme names can never be replaced.
    """
    if not isinstance(theme, Theme):
        raise TypeError(f"expected a Theme, got {type(theme).__name__}")
    key = theme.name.lower()
    if any(b.lower() == key for b in BUILTIN_THEMES):
        raise ValueError(
            f"cannot override built-in theme {theme.name!r}; choose another name"
        )
    if not overwrite and any(c.lower() == key for c in _CUSTOM_THEMES):
        raise ValueError(
            f"theme {theme.name!r} already registered; pass overwrite=True to replace"
        )
    _CUSTOM_THEMES[theme.name] = theme


def _reset_custom_themes() -> None:
    """Clear all registered custom themes (test helper)."""
    _CUSTOM_THEMES.clear()
