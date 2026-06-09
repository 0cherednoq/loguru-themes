---
title: Color scheme
description: Native loguru color tags follow the theme palette.
---

A theme isn't just a few accent colors — it carries a full 16-color ANSI
palette. When you apply it, loguru's **native color tags** are remapped to the
theme's palette, just like a terminal color scheme.

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "dracula")
logger.opt(colors=True).info("<red>danger</red> <blue>info</blue> <green>ok</green>")
# <red>/<blue>/<green> render in Dracula's colors. Switch to "monokai" and the
# same tags change accordingly.
```

This affects native tags in your **format strings** and in
`logger.opt(colors=True)` **messages**:

- foreground: `<red>`, short `<r>`, bright `<light-red>` …
- background: `<RED>`, short `<R>` …
- `<fg name>` / `<bg name>` alternative syntax

## Text vs background

Lowercase tags color the **text**; **uppercase** tags color the **background**.
A background tag alone does not change the text color, so set a foreground too
for readable contrast:

```python
logger.opt(colors=True).info("<black><GREEN> OK </GREEN></black>")
logger.opt(colors=True).info("<white><RED> ERROR </RED></white>")
```

## Control & scope

Remapping is process-global (that's what a color scheme is).

```python
# Don't touch loguru's standard colors:
apply_theme(logger, "dracula", remap_colors=False)

# Undo manually:
from loguru_themes import restore_palette
restore_palette()

# Scope it to a block (restored on exit):
from loguru_themes import using_palette, get_theme
with using_palette(get_theme("nord").palette):
    logger.opt(colors=True).info("<red>uses Nord red here</red>")
```

The palette is available as `theme.palette` (an `AnsiPalette`); set your own
with `theme.with_palette(AnsiPalette(...))`.
