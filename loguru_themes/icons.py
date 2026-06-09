"""Built-in Unicode icon sets for log levels."""

from __future__ import annotations

from .models import IconSet

# Minimalist standard-Unicode symbols, in the spirit of modern CLI tools.
DEFAULT_ICONS = IconSet(
    trace="›",  # ›
    debug="•",  # •
    info="•",  # •
    success="✔",  # ✔
    warning="!",
    error="✖",  # ✖
    critical="✖",  # ✖
)

# Every icon blank — used when icons are disabled.
NO_ICONS = IconSet(
    trace="",
    debug="",
    info="",
    success="",
    warning="",
    error="",
    critical="",
)
