---
title: API reference
description: Public functions and types — a quick usage reference.
---

Everything below is importable from `loguru_themes`.

## Functions

### `apply_theme(logger, theme, *, icons=True, sink=None, level="TRACE", colorize=None, replace=True, remap_colors=True)`

Configure `logger` with a theme's format, colors, and icons. Returns the loguru
handler id.

- **theme** — a built-in name, a registered name, or a `Theme`.
- **icons** — `True` (theme icons), `False` (none), an `IconSet`, or a mapping
  like `{"error": "!!"}`.
- **sink** — output sink; defaults to `sys.stderr`.
- **colorize** — `None` auto-detects the stream; `True`/`False` force it.
- **replace** — `True` removes existing handlers first (take over the console).
- **remap_colors** — `True` remaps native color tags to the theme palette.

### `get_theme(name) -> Theme`

Look up a theme by name (case-insensitive). Raises `KeyError` if unknown.

### `list_themes() -> list[str]`

All available theme names (built-in + registered), sorted.

### `register_theme(theme, *, overwrite=False)`

Register a custom `Theme` for lookup/apply by name. Built-in names are protected.

### `configure_levels(logger, theme, *, icons=True) -> Theme`

Register per-level color + icon on `logger` and add **no** sink.

### `build_format(theme, *, icons=True)`

Return the loguru `format` value for a theme (string or callable).

### Palette controls

- `install_palette(palette)` — remap loguru's native tags to a palette.
- `restore_palette()` — undo it.
- `using_palette(palette)` — context manager (restored on exit).
- `palette_active() -> bool`

## Types

### `Theme`

Fields: `name`, `levels` (`dict[str, LevelStyle]`), `accent`, `dim`, `fg`,
`icons` (`IconSet`), `fmt` (optional format override), `palette` (`AnsiPalette`).

Immutable `with_*` helpers (each returns a new `Theme`): `with_name`,
`with_accent`, `with_dim`, `with_fg`, `with_format`, `with_palette`,
`with_color`, `with_level`, `with_icon`, `with_icons`, `with_uniform_message`.

### `LevelStyle(color, bold=False, bg=None, msg_fg=None, msg_bg=None, msg_bold=False)`

How one level looks — the badge (`color`, `bold`, `bg`) and the message
(`msg_fg`, `msg_bg`, `msg_bold`). `.markup()` returns the loguru color token.

### `IconSet(trace, debug, info, success, warning, error, critical)`

Per-level Unicode symbols. `.get(level)` (case-insensitive) and
`.replace(mapping_or_kwargs)` for partial overrides.

### `AnsiPalette(black, red, green, yellow, blue, magenta, cyan, white, bright_*)`

The 16 named ANSI colors used for native-tag remapping.

### `ThemeName`

A `Literal` of the built-in theme names — used for IDE autocompletion.

## Constants

- `LEVELS` — the seven standard loguru level names.
- `DEFAULT_ICONS`, `NO_ICONS` — the default icon set and a blank one.
