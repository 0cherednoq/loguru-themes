"""Loguru format-string construction.

The default format is modeled on modern CLI tools (Claude Code / Codex CLI):
a dim timestamp, a colored level + icon, a dim ``module:line`` location, then
the message in the default foreground.
"""

from __future__ import annotations


def make_format(
    dim_hex: str,
    *,
    icons: bool = True,
    fg: str | None = None,
    message: str | None = None,
) -> str:
    """Build a loguru format string.

    ``dim_hex`` colors the timestamp and location. ``fg`` optionally colors the
    message text; when ``None`` the message keeps the terminal's default
    foreground. ``message`` overrides the whole message segment (used for
    per-level highlighting such as a red background on ERROR). When ``icons`` is
    False the ``{level.icon}`` slot is dropped entirely so alignment is
    preserved and no empty placeholder remains.
    """
    icon = "{level.icon} " if icons else ""
    if message is None:
        message = f"<fg {fg}>{{message}}</>" if fg else "{message}"
    return (
        f"<fg {dim_hex}>{{time:HH:mm:ss}}</> "
        f"<level>{icon}{{level.name: <8}}</level> "
        f"<fg {dim_hex}>{{name}}:{{line}}</> "
        f"{message}"
    )
