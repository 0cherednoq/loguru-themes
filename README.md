# loguru-themes

Curated color themes and minimalist Unicode level icons for [loguru](https://github.com/Delgan/loguru) — applied to any logger in a single call.

Themes are tuned after polished CLI tools (Claude Code, Codex CLI) and include JetBrains' **Dracula**.

📚 **Docs:** built with Astro Starlight in [`docs/`](docs/), bilingual (en/ru) (`cd docs && npm install && npm run dev`).
🤖 **For LLMs:** see [`llms.txt`](llms.txt).

## Install

```bash
pip install loguru-themes      # once published
# or, from a checkout:
pip install -e .
```

Requires Python 3.9+ and `loguru>=0.7`.

## Quickstart

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "dracula")

logger.info("server listening on http://localhost:8000")
logger.success("migration completed in 1.2s")
logger.warning("cache miss rate above 30%")
logger.error("failed to reach upstream service")
```

`apply_theme` takes over the logger's console output (it removes existing
handlers, the idiomatic loguru setup pattern) and installs a single themed
sink. Each level gets its theme color, and the level icon shares that color.

## Built-in themes

| Name         | Source                         |
|--------------|--------------------------------|
| `dracula`    | JetBrains / Dracula palette    |
| `nord`       | Nord                           |
| `catppuccin` | Catppuccin (Mocha)             |
| `monokai`    | Monokai                        |
| `dark`       | Neutral dark (CLI-style)       |
| `light`      | Neutral light (light terminals)|

```python
from loguru_themes import list_themes
list_themes()  # ['catppuccin', 'dark', 'dracula', 'light', 'monokai', 'nord']
```

## Icons

Default icons are plain Unicode (no Nerd Font needed): `›` `•` `•` `✔` `!` `✖` `✖`
for TRACE / DEBUG / INFO / SUCCESS / WARNING / ERROR / CRITICAL.

**Disable icons:**

```python
apply_theme(logger, "dracula", icons=False)
```

**Custom icon set:**

```python
from loguru_themes import IconSet, apply_theme

arrows = IconSet(
    trace="→", debug="→", info="→", success="✓",
    warning="▲", error="✕", critical="✕",
)
apply_theme(logger, "dracula", icons=arrows)
```

## Tweaking an existing theme

Like a built-in theme but want to change a few things? Themes are immutable —
each `with_*` helper returns a **new** theme, so you can chain them:

```python
from loguru import logger
from loguru_themes import apply_theme, get_theme

my_theme = (
    get_theme("dracula")
    .with_name("my-dracula")        # rename (e.g. before registering)
    .with_color("INFO", "#ffffff")  # change one level's color
    .with_icon("error", "!!")       # change one level's icon
    .with_fg("#e6e6e6")             # uniform message foreground
)
apply_theme(logger, my_theme)
```

Available helpers: `with_name`, `with_fg`, `with_accent`, `with_dim`,
`with_format`, `with_color(level, color)`, `with_level(level, **fields)`,
`with_icon(level, icon)`, `with_icons(set_or_mapping)`, and
`with_uniform_message(color=...)`.

**Make every message the same color** (drop the red ERROR / CRITICAL highlight):

```python
plain = get_theme("dracula").with_uniform_message("#e6e6e6")
apply_theme(logger, plain)
```

**Override a single level's full style** (badge + message):

```python
theme = get_theme("dracula").with_level(
    "WARNING", color="#ffd166", bold=True, msg_fg="#ffd166"
)
```

**Override just some icons inline at apply time** — no Theme needed:

```python
apply_theme(logger, "dracula", icons={"error": "!!", "warning": "▲"})
```

## Custom themes

```python
from loguru_themes import Theme, LevelStyle, register_theme, apply_theme

my_theme = Theme(
    name="my-theme",
    levels={
        "TRACE":    LevelStyle("#6b7280"),
        "DEBUG":    LevelStyle("#38bdf8"),
        "INFO":     LevelStyle("#e5e7eb"),
        "SUCCESS":  LevelStyle("#22c55e"),
        "WARNING":  LevelStyle("#f59e0b"),
        "ERROR":    LevelStyle("#ef4444"),
        "CRITICAL": LevelStyle("#f43f5e", bold=True),
    },
    accent="#38bdf8",
    dim="#6b7280",
)
register_theme(my_theme)
apply_theme(logger, "my-theme")
```

You can also pass a `Theme` directly without registering it:
`apply_theme(logger, my_theme)`.

## A theme is a real color scheme

A theme isn't just a few accent colors — it carries a full 16-color ANSI
palette. When you apply it, loguru's **native color tags** are remapped to the
theme's palette, exactly like a terminal color scheme:

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "dracula")
logger.opt(colors=True).info("<red>danger</red> <blue>info</blue> <green>ok</green>")
# <red>/<blue>/<green> now render in Dracula's red/blue/green — not the
# terminal's default 16 colors. Switch to "monokai" and the same tags change.
```

This affects native tags (`<red>`, `<blue>`, `<RED>` background, `<r>` short
forms, `<light-red>` …) in your format strings and in
`logger.opt(colors=True)` messages.

> **Tip:** lowercase tags color the text (`<green>`); **uppercase** tags color
> the background (`<GREEN>`). When using a background, also set a foreground so
> the text stays readable, e.g. `<black><GREEN> OK </GREEN></black>`.

- It's **process-global** (that's what a color scheme is). Disable per call with
  `apply_theme(..., remap_colors=False)`.
- Undo manually with `restore_palette()`, or scope it with the context manager:

  ```python
  from loguru_themes import using_palette, get_theme
  with using_palette(get_theme("nord").palette):
      ...  # native tags use Nord here; restored on exit
  ```

- Access or customize the palette: `theme.palette` (an `AnsiPalette`),
  `theme.with_palette(AnsiPalette(...))`, or `install_palette(palette)`.

## Use with your own logger setup

Don't want `apply_theme` to take over your logger? Use the building blocks it's
made of and keep full control of your own sinks and format.

**`configure_levels(logger, theme)`** registers the theme's per-level colors and
icons (via `logger.level(...)`) and adds **no sink**. Reference `<level>` and
`{level.icon}` in your own format:

```python
import sys
from loguru import logger
from loguru_themes import configure_levels

logger.remove()
configure_levels(logger, "dracula")          # colors + icons, no sink
logger.add(
    sys.stderr,
    format="<level>{level.icon} {level.name}</level> | {message}",  # your format
    colorize=True,
)
```

**`build_format(theme)`** hands you the format value the library would use (a
string, or a callable for themes with per-level message highlighting) so you can
drop it into your own `logger.add(...)` — your own file sink, rotation, etc.:

```python
from loguru_themes import configure_levels, build_format

configure_levels(logger, "dracula")
logger.add("app.log", format=build_format("dracula"), colorize=True, rotation="10 MB")
```

**Even lower level** — the raw markup for a single level and an icon, to wire by
hand:

```python
from loguru_themes import get_theme, resolve_icons

theme = get_theme("dracula")
logger.level("INFO", color=theme.levels["INFO"].markup(), icon=theme.icons.info)

icon_set, enabled = resolve_icons(theme, {"error": "!!"})  # resolve an icons spec
```

## Notes

- **Color & fallback:** by default `colorize=None` lets loguru auto-detect the
  stream — full truecolor on a terminal, plain text when redirected to a file or
  pipe (no raw markup tags). Force it with `colorize=True/False`.
- **Message color:** each theme sets a foreground color (`Theme.fg`) for the
  message text, so it looks consistent regardless of your terminal's default
  text color. Set `fg=None` on a custom theme to keep the terminal default.
- **ERROR / CRITICAL highlight:** ERROR renders the message text in red (like
  standard `logging`); CRITICAL renders it bold on a red background to stand out.
  Control it per level via `LevelStyle(msg_fg=..., msg_bg=..., msg_bold=...)`;
  leave them unset for a plain message.
- **Custom format / sink:** pass `sink=...`, `level=...`, or override the whole
  format string via `Theme(fmt=...)`.

## Examples

Three runnable scripts live in [`examples/`](examples/):

```bash
pip install -e .
python examples/01_quickstart.py     # apply a theme in one line
python examples/02_customize.py      # tweak a theme with the with_* API
python examples/03_color_scheme.py   # native tags follow the theme palette
```

More usage patterns (icons, custom themes, your own sinks/format, file logging)
are covered in the [docs](docs/).
