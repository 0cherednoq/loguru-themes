---
title: Customizing
description: Tweak a built-in theme or build your own.
---

## Tweak an existing theme

Themes are immutable — each `with_*` helper returns a **new** theme, so calls
chain and the original is never changed:

```python
from loguru import logger
from loguru_themes import apply_theme, get_theme

my_theme = (
    get_theme("dracula")
    .with_name("my-dracula")        # rename (e.g. before registering)
    .with_color("INFO", "#ffffff")  # one level's color
    .with_icon("error", "!!")       # one level's icon
    .with_fg("#e6e6e6")             # message text color
)
apply_theme(logger, my_theme)
```

Available helpers: `with_name`, `with_fg`, `with_accent`, `with_dim`,
`with_format`, `with_palette`, `with_color(level, color)`,
`with_level(level, **fields)`, `with_icon(level, icon)`,
`with_icons(set_or_mapping)`, and `with_uniform_message(color=...)`.

### One color for every message

Drop the red ERROR / CRITICAL highlight and use a single message color:

```python
plain = get_theme("dracula").with_uniform_message("#e6e6e6")
apply_theme(logger, plain)
```

### Restyle a single level

`with_level` sets any `LevelStyle` field — badge (`color`, `bold`, `bg`) and
message (`msg_fg`, `msg_bg`, `msg_bold`):

```python
theme = get_theme("dracula").with_level(
    "WARNING", color="#ffd166", bold=True, msg_fg="#ffd166"
)
```

## Build a theme from scratch

```python
from loguru_themes import Theme, LevelStyle, register_theme, apply_theme

ocean = Theme(
    name="ocean",
    levels={
        "TRACE":    LevelStyle("#5b7083"),
        "DEBUG":    LevelStyle("#48cae4"),
        "INFO":     LevelStyle("#90e0ef"),
        "SUCCESS":  LevelStyle("#52b788"),
        "WARNING":  LevelStyle("#ffb703"),
        "ERROR":    LevelStyle("#ef476f", msg_fg="#ef476f"),
        "CRITICAL": LevelStyle("#ff5d8f", bold=True,
                               msg_fg="#ffffff", msg_bg="#d00000", msg_bold=True),
    },
    accent="#48cae4",
    dim="#5b7083",
    fg="#caf0f8",
)
register_theme(ocean)
apply_theme(logger, "ocean")
```

You can also apply a `Theme` directly without registering it:
`apply_theme(logger, ocean)`.

### Registering

- `register_theme(theme)` makes it available by name via `apply_theme` /
  `get_theme`.
- Re-registering the same name needs `overwrite=True`.
- Built-in names can't be replaced.
