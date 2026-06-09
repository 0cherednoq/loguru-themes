## ADDED Requirements

### Requirement: 16-color ANSI palette

The system SHALL provide an `AnsiPalette` data structure defining the 16 standard terminal colors — the 8 base colors (`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`) and their 8 bright variants (`bright_*`) — as `#rrggbb` hex values. A `Theme` MAY carry an optional `palette`. Each built-in theme SHALL provide its canonical palette (e.g. the official Dracula palette).

#### Scenario: Built-in themes carry a palette

- **WHEN** a built-in theme such as `dracula` is looked up
- **THEN** its `palette` is a populated `AnsiPalette` of 16 validated hex colors

#### Scenario: Invalid palette color rejected

- **WHEN** an `AnsiPalette` is constructed with a non-hex value
- **THEN** the system raises a clear validation error

### Requirement: Native color tags follow the theme

When a theme with a palette is applied (and remapping is enabled), the system SHALL remap loguru's native color tags to the theme's palette, so that tags written by the user render in the theme's colors rather than the terminal's default 16. This SHALL cover foreground tags (`<red>`, long and short forms, and `<light-*>`), background tags (`<RED>` etc.), and the `<fg name>` / `<bg name>` alternative syntax, in both format strings and `logger.opt(colors=True)` messages.

#### Scenario: Foreground tag uses the theme color

- **WHEN** a theme is applied and a `<red>...</red>` tag is rendered
- **THEN** the text uses the theme palette's red (truecolor) and not the standard ANSI red

#### Scenario: Background tag uses the theme color

- **WHEN** a theme is applied and a `<GREEN>...</GREEN>` background tag is rendered
- **THEN** the background uses the theme palette's green

#### Scenario: Switching themes changes named colors

- **WHEN** the applied theme changes from `dracula` to `monokai`
- **THEN** the same `<red>` tag renders in each theme's respective red

### Requirement: Remapping is controllable and reversible

Native-color remapping is process-global and SHALL be controllable. `apply_theme(..., remap_colors=False)` SHALL leave loguru's standard colors untouched. The system SHALL provide `install_palette(palette)`, `restore_palette()`, a `using_palette(palette)` context manager, and `palette_active()`. Applying a theme without a palette while remapping is enabled SHALL restore the defaults. If loguru's internals are unavailable, remapping SHALL be skipped without crashing.

#### Scenario: Opt out of remapping

- **WHEN** `apply_theme(logger, "dracula", remap_colors=False)` is called
- **THEN** native tags such as `<red>` still render the standard ANSI red

#### Scenario: Restore standard colors

- **WHEN** `restore_palette()` is called after a palette was installed
- **THEN** `palette_active()` is False and native tags render their standard ANSI colors again

#### Scenario: Scoped remapping

- **WHEN** code runs inside `with using_palette(theme.palette):`
- **THEN** native tags use the theme palette inside the block and are restored on exit
