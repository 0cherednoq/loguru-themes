---
title: Themes
description: The built-in themes and how to list and choose them.
---

## Built-in themes

| Name         | Source                          |
| ------------ | ------------------------------- |
| `dracula`    | JetBrains / Dracula palette     |
| `nord`       | Nord                            |
| `catppuccin` | Catppuccin (Mocha)              |
| `monokai`    | Monokai                         |
| `dark`       | Neutral dark (CLI-style)        |
| `light`      | Neutral light (light terminals) |

Apply any of them by name:

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "monokai")
```

## Previews

Sample output of every level under each theme (the theme name is shown in each
window's title bar):

![dracula theme log output](../../assets/themes/dracula.svg)

![nord theme log output](../../assets/themes/nord.svg)

![catppuccin theme log output](../../assets/themes/catppuccin.svg)

![monokai theme log output](../../assets/themes/monokai.svg)

![dark theme log output](../../assets/themes/dark.svg)

![light theme log output](../../assets/themes/light.svg)

## Logs with colored backgrounds

Highlight tags on background colors from the palette (text auto-contrasted):

![dracula logs with colored backgrounds](../../assets/themes/dracula-bg.svg)

![nord logs with colored backgrounds](../../assets/themes/nord-bg.svg)

![catppuccin logs with colored backgrounds](../../assets/themes/catppuccin-bg.svg)

![monokai logs with colored backgrounds](../../assets/themes/monokai-bg.svg)

![dark logs with colored backgrounds](../../assets/themes/dark-bg.svg)

![light logs with colored backgrounds](../../assets/themes/light-bg.svg)

## Palette (background colors)

The 16-color palette of each theme — the colors native tags like `<red>` /
`<RED>` map to:

![dracula palette](../../assets/themes/dracula-palette.svg)

![nord palette](../../assets/themes/nord-palette.svg)

![catppuccin palette](../../assets/themes/catppuccin-palette.svg)

![monokai palette](../../assets/themes/monokai-palette.svg)

![dark palette](../../assets/themes/dark-palette.svg)

![light palette](../../assets/themes/light-palette.svg)

## Listing themes

```python
from loguru_themes import list_themes

list_themes()
# ['catppuccin', 'dark', 'dracula', 'light', 'monokai', 'nord']
```

Names are case-insensitive (`"Dracula"` works). An unknown name raises a
`KeyError` listing the available names.

## Getting a theme object

```python
from loguru_themes import get_theme

theme = get_theme("dracula")
theme.levels["INFO"].color   # '#bd93f9'
theme.accent, theme.dim, theme.fg
```

Useful when you want to inspect or [customize](../customizing/) a theme, or
reference its colors in your [own format](../own-logger/).

## Highlights

- **ERROR** renders the message text in red (like the standard `logging` look).
- **CRITICAL** renders the message bold on a red background to stand out.

Both are configurable per level — see [Customizing](../customizing/).

## Light vs dark

`dark`/`light` are tuned for dark/light terminal backgrounds respectively;
`dracula`, `nord`, `catppuccin`, and `monokai` are dark-background palettes.
