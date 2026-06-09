## ADDED Requirements

### Requirement: Per-level Unicode icon set

The system SHALL define an `IconSet` mapping each standard loguru level (`TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`) to a minimalist Unicode symbol (e.g. `›`, `•`, `ℹ`/`•`, `✔`, `!`/`⚠`, `✖`, `✖`). Icons MUST be plain Unicode (no Nerd Font / private-use glyphs) so they render in standard terminals without extra fonts.

#### Scenario: Every level has an icon

- **WHEN** the default icon set is inspected
- **THEN** each of the seven standard loguru levels maps to exactly one Unicode symbol

#### Scenario: Icons are standard Unicode

- **WHEN** any default icon is examined
- **THEN** it is a standard Unicode codepoint (not in a Nerd Font private-use range)

### Requirement: Icons render with the theme

The system SHALL render the level's icon as part of each log line when a theme is applied, colored with that level's theme color so the icon and level share a consistent hue.

#### Scenario: Icon appears in output

- **WHEN** a record is logged at `SUCCESS` under an applied theme
- **THEN** the rendered line includes the `SUCCESS` icon colored with the theme's `SUCCESS` color

#### Scenario: Icon color matches level

- **WHEN** records are logged at `WARNING` and `ERROR`
- **THEN** each line's icon is colored with the corresponding level color, matching the level text

### Requirement: Icon overriding and disabling

The system SHALL allow a caller to override icons three ways and to disable them entirely: (a) a full custom `IconSet`; (b) a partial override via `IconSet.replace(mapping_or_kwargs)` or a theme's `with_icon`/`with_icons` helpers; (c) an inline mapping passed to `apply_theme(..., icons={...})`. When icons are disabled, output SHALL remain correctly aligned and free of leftover icon placeholders. Icon overrides SHALL accept case-insensitive level names and reject unknown levels.

#### Scenario: Custom icon set

- **WHEN** a custom `IconSet` is supplied to `apply_theme`
- **THEN** rendered lines use the custom symbols instead of the defaults

#### Scenario: Partial override keeps the rest

- **WHEN** a caller overrides only some icons (e.g. `icons.replace(error="!!")` or `theme.with_icons({"warning": "▲"})`)
- **THEN** the named levels use the new symbols and all other levels keep the theme's icons

#### Scenario: Inline override at apply time

- **WHEN** `apply_theme(logger, "dracula", icons={"info": ">>"})` is called
- **THEN** INFO uses `>>` and the other levels keep the theme's icons

#### Scenario: Unknown level rejected

- **WHEN** an icon override targets a non-existent level name
- **THEN** the system raises a clear error

#### Scenario: Icons disabled

- **WHEN** a theme is applied with `icons=False`
- **THEN** log lines render without any icon and contain no empty icon slot or stray markup
