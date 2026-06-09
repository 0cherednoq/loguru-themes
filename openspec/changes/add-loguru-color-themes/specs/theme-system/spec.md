## ADDED Requirements

### Requirement: Theme data model

The system SHALL provide a `Theme` data structure defining: a unique `name`; a mapping of loguru log levels (`TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`) to `LevelStyle` values; `accent` and `dim` colors for non-level parts of a line; an optional `fg` color for the message text; an `IconSet`; an optional `palette` (`AnsiPalette`); and an optional format-string override `fmt`. A `LevelStyle` SHALL describe the level badge (`color`, `bold`, optional background `bg`) and the message (`msg_fg`, `msg_bg`, `msg_bold`). Colors SHALL be `#rrggbb` hex and SHALL be validated.

#### Scenario: Constructing a theme

- **WHEN** a `Theme` is created with a name, a complete per-level mapping, accent/dim colors, and (optionally) fg/icons/palette
- **THEN** the object exposes those fields and is accepted by `apply_theme` without error

#### Scenario: Incomplete level mapping is rejected

- **WHEN** a `Theme` is constructed missing one or more standard loguru levels
- **THEN** the system raises a clear error naming the missing level(s)

#### Scenario: Invalid color is rejected

- **WHEN** a `LevelStyle` or theme color is constructed with a value that is not `#rrggbb` hex
- **THEN** the system raises a clear validation error

### Requirement: Built-in theme registry

The system SHALL ship a registry of built-in themes accessible by name. The registry MUST include at least: `dracula` (JetBrains/Dracula), `nord`, `catppuccin`, `monokai`, a neutral `dark`, and a neutral `light`. Theme names SHALL be case-insensitive on lookup.

#### Scenario: Look up a built-in theme by name

- **WHEN** a caller requests a theme by a known name (e.g. `"dracula"` or `"Dracula"`)
- **THEN** the corresponding `Theme` object is returned

#### Scenario: Unknown theme name

- **WHEN** a caller requests a theme name that does not exist
- **THEN** the system raises an error listing the available theme names

#### Scenario: Listing available themes

- **WHEN** a caller lists available themes
- **THEN** the system returns all built-in theme names including `dracula`, `nord`, `catppuccin`, `monokai`, `dark`, and `light`

### Requirement: Apply a theme to a logger

The system SHALL provide `apply_theme(logger, theme, *, icons=True, sink=None, level="TRACE", colorize=None, replace=True, remap_colors=True)` that configures `logger` so subsequent log calls render with the theme's format, per-level colors, and icons. `theme` SHALL accept a theme name string or a `Theme`. By default (`replace=True`) it SHALL remove existing handlers and install a single themed sink; applying it MUST NOT stack duplicate sinks.

#### Scenario: Apply by name

- **WHEN** `apply_theme(logger, "dracula")` is called
- **THEN** subsequent records at every level are emitted using the Dracula colors, format, and icons

#### Scenario: Apply by Theme object

- **WHEN** `apply_theme(logger, theme_obj)` is called with a `Theme` instance
- **THEN** the logger renders using that theme

#### Scenario: Re-applying does not duplicate output

- **WHEN** `apply_theme` is called twice on the same logger
- **THEN** each log line is emitted exactly once

#### Scenario: Per-level colors are distinct

- **WHEN** records are logged at `INFO`, `WARNING`, and `ERROR` under an applied theme
- **THEN** each level's output uses its theme-defined color

### Requirement: Message foreground color

The system SHALL color the message text using the theme's `fg` color when set, so appearance is consistent regardless of the terminal's default text color. When `fg` is unset, the message SHALL keep the terminal's default foreground.

#### Scenario: Message uses theme foreground

- **WHEN** a theme with a defined `fg` is applied and a record is logged
- **THEN** the message text is rendered in that `fg` color

### Requirement: Per-level message highlighting

The system SHALL support per-level highlighting of the message text via `LevelStyle.msg_fg` / `msg_bg` / `msg_bold`. Built-in themes SHALL render ERROR message text in red and CRITICAL message text bold on a red background. Themes that use message highlighting SHALL still render exception tracebacks correctly.

#### Scenario: ERROR message is red

- **WHEN** a record is logged at ERROR under a built-in theme
- **THEN** the message text is rendered in the theme's red foreground (no background)

#### Scenario: CRITICAL message is highlighted

- **WHEN** a record is logged at CRITICAL under a built-in theme
- **THEN** the message text is rendered bold on the theme's red background

#### Scenario: Exceptions still render

- **WHEN** an exception is logged (e.g. `logger.exception(...)`) under a highlighting theme
- **THEN** the traceback is rendered and the message line is not duplicated

### Requirement: Custom theme registration

The system SHALL allow callers to register a custom `Theme` for later lookup/apply by name. Registering an existing custom name SHALL require explicit `overwrite=True`. Built-in theme names MUST NOT be replaceable, and the built-in defaults MUST NOT be corrupted.

#### Scenario: Register and apply a custom theme

- **WHEN** a caller registers a custom `Theme` named `"my-theme"` and then calls `apply_theme(logger, "my-theme")`
- **THEN** the logger renders using the custom theme

#### Scenario: Built-in names are protected

- **WHEN** a caller registers a theme whose name collides with a built-in (e.g. `"dracula"`)
- **THEN** the system raises an error and the built-in remains unchanged

### Requirement: Theme customization API

The system SHALL provide an immutable customization API on `Theme`: each `with_*` helper returns a new `Theme` and leaves the original unchanged. The API SHALL include at least: `with_name`, `with_accent`, `with_dim`, `with_fg`, `with_format`, `with_palette`, `with_color(level, color)`, `with_level(level, **fields)`, `with_icon(level, icon)`, `with_icons(set_or_mapping)`, and `with_uniform_message(color=...)`. Level-targeting helpers SHALL reject unknown level names.

#### Scenario: Derivation is immutable and chainable

- **WHEN** a caller chains `get_theme("dracula").with_color("INFO", "#ffffff").with_icon("error", "!!")`
- **THEN** a new theme carries both overrides and the original `dracula` theme is unchanged

#### Scenario: Uniform message style

- **WHEN** a caller applies `theme.with_uniform_message("#cccccc")`
- **THEN** every level's message renders in that one color with no per-level highlighting

#### Scenario: Unknown level rejected

- **WHEN** a caller calls `with_level`/`with_color`/`with_icon` with a non-existent level name
- **THEN** the system raises a clear error

### Requirement: Low-level building blocks

The system SHALL expose the pieces `apply_theme` is composed of so callers can integrate a theme into their own logger setup: `configure_levels(logger, theme, *, icons=True)` SHALL register per-level color and icon via `logger.level(...)` and add **no** sink; `build_format(theme, *, icons=True)` SHALL return the loguru `format` value (a string, or a callable for themes with message highlighting) suitable for the caller's own `logger.add(...)`. A `Theme` SHALL also expose raw pieces (`levels[name].markup()`, `icons.get(level)`, `accent`/`dim`/`fg`).

#### Scenario: Configure levels without adding a sink

- **WHEN** `configure_levels(logger, "dracula")` is called and the caller then adds their own sink referencing `<level>` and `{level.icon}`
- **THEN** the caller's output uses the theme's colors and icons, and no sink was added by `configure_levels`

#### Scenario: Reuse the format in a custom sink

- **WHEN** a caller passes `build_format("dracula")` as the `format` of their own `logger.add(...)`
- **THEN** records render with the theme's format

### Requirement: Loguru colorization and graceful fallback

The system SHALL configure the sink so theme markup renders as ANSI color on a color-capable stream, and SHALL degrade gracefully (readable plain text, no raw markup tags) when the stream does not support color. By default `colorize` SHALL auto-detect the stream.

#### Scenario: Colorized terminal

- **WHEN** a theme is applied to a logger writing to a color-capable terminal
- **THEN** output contains ANSI color sequences corresponding to the theme

#### Scenario: Non-color stream

- **WHEN** output is redirected to a non-color stream (e.g. a file or pipe)
- **THEN** log lines are readable plain text with no raw markup tags
