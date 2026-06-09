---
title: Icons
description: Per-level Unicode icons — disable, replace, or override inline.
---

Each theme renders a minimalist Unicode icon next to the level. Defaults
(no special fonts required):

| Level    | Icon |
| -------- | ---- |
| TRACE    | `›`  |
| DEBUG    | `•`  |
| INFO     | `•`  |
| SUCCESS  | `✔`  |
| WARNING  | `!`  |
| ERROR    | `✖`  |
| CRITICAL | `✖`  |

## Disable icons

```python
apply_theme(logger, "dracula", icons=False)
```

Alignment is preserved — no empty icon slot is left behind.

## Override some icons inline

Pass a mapping to change only certain levels; the rest keep the theme's icons:

```python
apply_theme(logger, "dracula", icons={"error": "💥", "info": "i"})
```

## A full custom icon set

```python
from loguru_themes import IconSet, apply_theme

arrows = IconSet(
    trace="→", debug="→", info="→", success="✓",
    warning="▲", error="✕", critical="✕",
)
apply_theme(logger, "dracula", icons=arrows)
```

## On a theme

You can also bake icon changes into a theme (see [Customizing](../customizing/)):

```python
from loguru_themes import get_theme, apply_theme

theme = get_theme("dracula").with_icon("error", "!!")
apply_theme(logger, theme)
```
