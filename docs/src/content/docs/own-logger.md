---
title: Use your own logger
description: Keep your own sinks and format using the theme building blocks.
---

`apply_theme` is convenient but takes over the logger. When you want your own
sinks or format, use the building blocks it's made of.

## `configure_levels` — colors + icons, no sink

Registers the theme's per-level color and icon (via `logger.level(...)`) and
adds **no** sink. Reference `<level>` and `{level.icon}` in your own format:

```python
import sys
from loguru import logger
from loguru_themes import configure_levels

logger.remove()
configure_levels(logger, "dracula")           # colors + icons, no sink
logger.add(
    sys.stderr,
    format="<level>{level.icon} {level.name}</level> | {message}",
    colorize=True,
)
```

## `build_format` — the theme's format value

Hands you the loguru `format` value (a string, or a callable for themes with
per-level message highlighting) for your own `logger.add(...)`:

```python
from loguru_themes import configure_levels, build_format

configure_levels(logger, "dracula")
logger.add("app.log", format=build_format("dracula"), colorize=True, rotation="10 MB")
```

## Reference theme colors in a custom format

You don't hardcode hex — read it from the theme. `<level>` auto-uses the
current level's color; for fixed parts interpolate `theme.accent` / `dim` / `fg`:

```python
from loguru_themes import get_theme, configure_levels

theme = get_theme("dracula")
fmt = (
    f"<fg {theme.accent}>┃</>"
    f" <fg {theme.dim}>{{time:HH:mm:ss}}</>"
    f" <level>{{level.icon}} {{level.name: <8}}</level>"
    f" <fg {theme.fg}>{{message}}</>"
)
configure_levels(logger, theme)
logger.add(sys.stderr, format=fmt, colorize=True, level="TRACE")
```

A single level's raw color token: `theme.levels["ERROR"].markup()` → `'<fg #ff5555>'`.

## Console + file

`colorize=None` (the default) auto-detects the stream: color on a terminal,
plain text in a file — no raw markup tags.

```python
configure_levels(logger, "dracula")
fmt = build_format("dracula")
logger.add(sys.stderr, format=fmt, colorize=True)    # colored console
logger.add("app.log", format=fmt, colorize=False)    # plain file
```
