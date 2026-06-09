## Context

`loguru_themes` is a greenfield Python library (currently only a PyCharm placeholder `main.py`). Goal: ship curated, beautiful color themes plus per-level Unicode icons for `loguru`, applied through a single `apply_theme(logger, theme)` call.

Key facts about loguru that shape the design:
- A sink is added with `logger.add(sink, format=..., colorize=True, level=...)`.
- loguru format markup supports named colors, hex (`<fg #bd93f9>`), and `<level>...</level>` which applies the color registered for the *current record's* level.
- Per-level appearance is set with `logger.level(name, color=..., icon=...)`. **loguru natively stores a per-level `icon`**, accessible in formats as `{level.icon}`. This is the cleanest integration point for our icons.
- `logger.add` returns a handler id; passing it to `logger.remove(id)` removes exactly that sink.

## Goals / Non-Goals

**Goals:**
- Curated built-in themes: `dracula` (JetBrains), `nord`, `catppuccin`, `monokai`, neutral `dark`, neutral `light`.
- Minimalist Unicode icons per level, colored to match the level.
- One-call API `apply_theme(logger, theme)` accepting a name or a `Theme`.
- Idempotent application (no duplicate sinks), custom theme registration, graceful no-color fallback.

**Non-Goals:**
- Nerd Font / private-use glyph icon sets (explicitly chosen against; Unicode only).
- Theming non-loguru loggers (stdlib `logging`) — out of scope for v1.
- Auto-detecting the user's terminal theme or syncing with OS dark/light mode.
- File-rotation, structured/JSON sinks, or any sink concern beyond color+format.

## Decisions

### D1 — Theme model as a frozen dataclass
`Theme(name, levels: dict[str, LevelStyle], accent, dim, fmt, icons: IconSet)`, where `LevelStyle` holds a loguru color string (and implicitly the level icon comes from `icons`). Frozen/immutable so built-ins can't be mutated in place. Validation in `__post_init__` ensures all seven levels are present (satisfies "incomplete mapping is rejected").
*Alternative considered:* plain dicts — rejected, no validation and weak typing.

### D2 — Apply via `logger.level()` + a single `add()`
`apply_theme` will, in order:
1. Remove the previously library-managed handler if one exists (tracked in a module-level registry keyed by `id(logger)`), so re-applying does not stack sinks.
2. For each level, call `logger.level(name, color=<theme color>, icon=<icon or "">)`.
3. `logger.add(sys.stderr, format=theme.fmt, colorize=True, level=lowest_level)` and store the returned handler id.

The format string uses `<level>{level.icon} {level.name: <8}</level>` so the icon inherits the level color automatically — this is why icon+level share a hue without extra markup.
*Alternative considered:* injecting icons via a `patch()`/filter function — rejected as more complex than loguru's built-in `{level.icon}`.

### D3 — Format string shape (modeled on modern CLI tools)
Default format, tuned to look like Claude Code / Codex CLI output (dim timestamp, colored level+icon, dim location separator):
```
<dim>{time:HH:mm:ss}</dim> <level>{level.icon} {level.name:<8}</level> <dim>{name}:{line}</dim> {message}
```
`<dim>` maps to the theme's `dim` color; the message stays default foreground for readability. Themes may override the whole format string.

### D4 — Built-in palettes (hex per level)
Colors drawn from each theme's canonical palette.

| Level    | dracula  | nord     | catppuccin | monokai  | dark (CLI) | light (CLI) |
|----------|----------|----------|------------|----------|------------|-------------|
| TRACE    | #6272a4  | #4c566a  | #6c7086    | #75715e  | #6b7280    | #9ca3af     |
| DEBUG    | #8be9fd  | #88c0d0  | #89dceb    | #66d9ef  | #38bdf8    | #0284c7     |
| INFO     | #bd93f9  | #81a1c1  | #cba6f7    | #a6e22e  | #e5e7eb    | #1f2937     |
| SUCCESS  | #50fa7b  | #a3be8c  | #a6e3a1    | #a6e22e  | #22c55e    | #16a34a     |
| WARNING  | #ffb86c  | #ebcb8b  | #f9e2af    | #e6db74  | #f59e0b    | #b45309     |
| ERROR    | #ff5555  | #bf616a  | #f38ba8    | #f92672  | #ef4444    | #dc2626     |
| CRITICAL | #ff79c6* | #b48ead* | #eba0ac*   | #f92672* | #f43f5e*   | #be123c*    |
| accent   | #bd93f9  | #88c0d0  | #cba6f7    | #66d9ef  | #38bdf8    | #2563eb     |
| dim      | #6272a4  | #4c566a  | #6c7086    | #75715e  | #6b7280    | #9ca3af     |

`*` CRITICAL is rendered **bold** (`<bold><fg #...>`) to stand apart from ERROR.

### D5 — Default Unicode icon set
`TRACE ›`, `DEBUG •`, `INFO •`, `SUCCESS ✔`, `WARNING !`, `ERROR ✖`, `CRITICAL ✖`. All standard Unicode (no Nerd Font). Overridable via a custom `IconSet`; `icons=False`/disabled yields `icon=""` for every level and a format that drops the icon slot so alignment is preserved.

### D6 — Public API surface
`apply_theme(logger, theme, *, icons=True, sink=None, level="TRACE", colorize=None, replace=True, remap_colors=True)`, `get_theme(name)`, `list_themes()`, `register_theme(theme, *, overwrite=False)`, plus exported `Theme`, `LevelStyle`, `IconSet`, `AnsiPalette`. Registry lookup is case-insensitive; unknown names raise `KeyError` listing available names.

### D7 — Message foreground (`Theme.fg`)
The message text is colored with the theme's `fg` so appearance does not depend on the terminal's default text color. `fg=None` keeps the terminal default. `make_format` gained a `message` segment override to support this and per-level highlighting.
*Alternative:* leaving messages uncolored — rejected because the terminal default could be any color (e.g. red), making logs look broken.

### D8 — Per-level message highlighting + callable format
`LevelStyle` carries `msg_fg`/`msg_bg`/`msg_bold` for the message (distinct from the badge's `color`/`bold`/`bg`). Because the highlight depends on the record's level, `build_format` returns a **callable** formatter for themes that use highlighting (a static string otherwise). A callable format must append `"\n{exception}"` itself (loguru does not auto-append for callables) — verified so tracebacks render. Built-ins: ERROR = red text; CRITICAL = bold on red background.

### D9 — Ergonomic, immutable customization
`Theme` is frozen; `with_*` helpers (`with_color`, `with_icon`, `with_icons`, `with_fg`, `with_uniform_message`, `with_level`, `with_palette`, …) return new themes via `dataclasses.replace`, so originals are never mutated and calls chain. `IconSet.replace(...)` supports partial icon overrides; `apply_theme(icons=...)` also accepts a partial mapping.
*Alternative:* a single `customize(**kwargs)` — rejected as less discoverable than focused, chainable methods.

### D10 — Low-level building blocks
`apply_theme` = `configure_levels` (register per-level color+icon, no sink) + `build_format` (the loguru `format` value) + `logger.add`. Exposing the first two lets users keep their own sinks/format. Raw pieces (`LevelStyle.markup()`, `IconSet.get()`, `theme.accent/dim/fg`) are public so a hand-written format can reference theme colors instead of hardcoding hex.

### D11 — Theme as a real color scheme (native-tag remapping)
A theme carries a 16-color `AnsiPalette`. On apply (default `remap_colors=True`), loguru's native color tags (`<red>`, `<blue>`, `<RED>`, short/`<light-*>` forms) are remapped to the palette by patching the class-level color tables in `loguru._colorizer.AnsiParser` (plain `{name: escape}` dicts) to truecolor escapes. This is **process-global** — matching the "color scheme" mental model — isolated in `palette.py`, guarded by `try/except` on the loguru import, saved/restored via `install_palette`/`restore_palette`/`using_palette`.
*Alternative:* a per-handler hook — loguru exposes none, so monkeypatching the documented-but-internal tables is the only route; the coupling is contained and reversible.

## Risks / Trade-offs

- **Mutating global level config** → `logger.level()` changes are process-global, so applying a theme affects every handler on that logger. *Mitigation:* documented behavior; `apply_theme` is the intended single configuration point. Re-applying restores a consistent state.
- **Color accuracy depends on the terminal palette** → hex colors render via ANSI truecolor; terminals limited to 256/16 colors approximate them. *Mitigation:* chosen palettes are legible even when approximated; `colorize=True` + loguru handle downgrade.
- **`light` theme on dark terminals** → light-optimized colors may have low contrast on dark backgrounds. *Mitigation:* documented as intended for light-background terminals.
- **Icon width** → some glyphs render as double-width in certain fonts, misaligning columns. *Mitigation:* default set uses narrow symbols; format pads the level name, not the icon, and icons can be disabled.
- **No-color streams** → ANSI escapes in a redirected file. *Mitigation:* `colorize` defaults to `None` (auto-detect), so loguru emits color only on a tty and strips markup otherwise; covered by a spec scenario and a test.
- **Global native-tag remapping** → patching `loguru._colorizer.AnsiParser` is process-wide and touches a loguru internal. *Mitigation:* opt-out via `remap_colors=False`; fully reversible via `restore_palette()`/`using_palette`; the import is guarded so a loguru change degrades to "no remap + warning" rather than a crash. Confined to `palette.py`.

## Migration Plan

Greenfield — no migration. The placeholder `main.py` is replaced by a runnable example/demo that prints all levels under each theme. Adopters install the package and call `apply_theme(logger, "dracula")`.

## Open Questions

- Should `dark`/`light` auto-select based on a `NO_COLOR` / terminal-background hint? Deferred to a later change; v1 requires explicit choice.
- Whether to expose a screenshot-generation helper for docs — nice-to-have, not in scope for v1.
