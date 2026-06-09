## Why

`loguru` produces readable logs out of the box, but making them *beautiful* and *consistent* requires hand-crafting color markup and format strings in every project. There is no curated set of polished, ready-to-use color themes — the kind of carefully tuned palettes that modern CLI tools (Claude Code, Codex CLI, etc.) use to make terminal output pleasant and scannable. This library provides a small, batteries-included set of high-quality themes (including JetBrains' Dracula) plus per-level Unicode icons, applied to any loguru logger with a single call.

## What Changes

- Introduce a **theme data model**: per-level styles (`LevelStyle`: badge color/bold/background **and** message foreground/background/bold), accent/dim/foreground colors, an optional format string, an icon set, and a 16-color ANSI palette.
- Ship a **built-in theme registry** with curated palettes: `dracula` (JetBrains), `nord`, `catppuccin`, `monokai`, plus neutral `dark` and `light` themes modeled on modern CLI tooling (Claude Code / Codex CLI).
- Add **per-level Unicode icons** (minimalist symbols such as `✔ ✖ ! • ›`), overridable wholesale, per-level, or inline at apply time; disengageable without breaking alignment.
- **Highlight severe levels**: the message text renders red for ERROR and bold on a red background for CRITICAL; configurable per level.
- Provide the primary public API **`apply_theme(logger, theme)`** that configures a loguru sink (format, colors, icons) on a given logger, accepting a theme name or a `Theme`.
- Expose **low-level building blocks** — `configure_levels(logger, theme)` (colors+icons, no sink) and `build_format(theme)` (the loguru format value) — so users can wire their own `logger.add(...)`.
- Provide an **ergonomic customization API**: immutable `with_*` derivations (`with_color`, `with_icon`, `with_icons`, `with_fg`, `with_uniform_message`, `with_level`, `with_palette`, …).
- Make a theme behave as a **real color scheme**: when applied, loguru's native color tags (`<red>`, `<blue>`, `<RED>`, …) are remapped to the theme's ANSI palette.
- Provide helpers to **list/look up** themes and **register custom themes**.
- Package the project as an installable Python library (`loguru_themes`) with a clean public surface and example usage.

## Capabilities

### New Capabilities
- `theme-system`: The theme data model, built-in registry, custom-theme registration, the `apply_theme(logger, theme)` API and its low-level building blocks (`configure_levels`, `build_format`), per-level message highlighting, and the immutable `with_*` customization API.
- `level-icons`: Per-level Unicode icon sets, their integration into rendered output, overriding (wholesale / per-level / inline mapping), and disabling behavior.
- `ansi-color-scheme`: The 16-color `AnsiPalette` and remapping of loguru's native color tags to it, so an applied theme acts as a full terminal color scheme; with scoped install/restore controls.

### Modified Capabilities
<!-- None — greenfield project, no existing specs. -->

## Impact

- **New code**: `loguru_themes` package — `models` (Theme/LevelStyle/IconSet/AnsiPalette), `themes`, `registry`, `icons`, `formats`, `apply`, and `palette` (loguru native-tag remapping). Replaces the placeholder `main.py`.
- **Dependencies**: adds `loguru` as a runtime dependency.
- **Packaging**: introduces project metadata (`pyproject.toml`) for an installable library.
- **Side effects**: native-color-tag remapping patches loguru's internal color tables process-wide (opt-out via `remap_colors=False`, reversible via `restore_palette()`).
- **No breaking changes** (greenfield); the only consumer touched is the sample `main.py`, which becomes an example/demo.
