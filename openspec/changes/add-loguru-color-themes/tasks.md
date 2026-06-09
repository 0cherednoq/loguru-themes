## 1. Project scaffolding

- [x] 1.1 Add `pyproject.toml` with package metadata for `loguru_themes` and `loguru` as a runtime dependency
- [x] 1.2 Create the `loguru_themes/` package directory with `__init__.py` exporting the public API (`apply_theme`, `get_theme`, `list_themes`, `register_theme`, `Theme`, `LevelStyle`, `IconSet`)

## 2. Data model

- [x] 2.1 Implement `LevelStyle` (color string + bold flag) and `IconSet` (per-level Unicode symbol mapping) in `models.py`
- [x] 2.2 Implement frozen `Theme` dataclass (name, levels, accent, dim, fmt, icons) with `__post_init__` validation that all seven loguru levels are present, raising a clear error naming missing levels

## 3. Icons

- [x] 3.1 Define the default Unicode `IconSet` (`› • • ✔ ! ✖ ✖`) and assert no Nerd Font / private-use codepoints
- [x] 3.2 Implement icon disabling (empty icons + format variant) and custom `IconSet` override plumbing

## 4. Built-in themes

- [x] 4.1 Implement the default CLI-style format string and a `<dim>`-aware variant for the no-icon case (per design D3)
- [x] 4.2 Define `dracula`, `nord`, `catppuccin`, `monokai`, `dark`, and `light` themes using the hex palettes in design D4 (CRITICAL rendered bold)

## 5. Registry & apply

- [x] 5.1 Implement the theme registry: `get_theme` (case-insensitive, `KeyError` listing names on miss), `list_themes`, and `register_theme(overwrite=False)` that never corrupts built-in defaults
- [x] 5.2 Implement `apply_theme(logger, theme, *, icons=True)`: track the library-managed handler per logger, remove the prior one on re-apply, set per-level `color`/`icon` via `logger.level(...)`, and add a colorized `sys.stderr` sink

## 6. Demo & docs

- [x] 6.1 Replace `main.py` with a runnable demo that logs every level under each built-in theme
- [x] 6.2 Write `README.md` with install, quickstart (`apply_theme(logger, "dracula")`), the theme list, and icon override/disable examples

## 7. Tests

- [x] 7.1 Tests for `Theme` validation (missing-level rejection) and registry lookup (case-insensitive hit, unknown-name error lists available themes)
- [x] 7.2 Tests that `apply_theme` is idempotent (no duplicate lines on re-apply) and that each level renders its distinct color
- [x] 7.3 Tests that icons appear and share the level color, custom `IconSet` overrides apply, and disabled icons leave no stray markup
- [x] 7.4 Test graceful no-color fallback: output to a non-tty stream contains no raw markup tags

## 8. Message foreground & per-level highlighting

- [x] 8.1 Add `Theme.fg` and color the message with it; extend `make_format` with a `message` segment override; default to terminal fg when unset
- [x] 8.2 Add `LevelStyle.msg_fg`/`msg_bg`/`msg_bold` and a `message_wrap()` helper
- [x] 8.3 Make `build_format` return a per-record callable when a theme uses message highlighting, appending `\n{exception}` so tracebacks render
- [x] 8.4 Built-in highlighting: ERROR red message text; CRITICAL bold on red background
- [x] 8.5 Tests: ERROR red foreground (no bg), CRITICAL background, exceptions still render

## 9. Immutable customization API

- [x] 9.1 Add chainable `with_*` helpers to `Theme` (`with_name`, `with_accent`, `with_dim`, `with_fg`, `with_format`, `with_color`, `with_level`, `with_icon`, `with_icons`, `with_uniform_message`, `with_palette`)
- [x] 9.2 Add `IconSet.replace(...)` (partial, case-insensitive) and accept a partial icon mapping in `apply_theme(icons=...)`
- [x] 9.3 Validate/reject unknown level names in level-targeting helpers
- [x] 9.4 Tests: immutability + chaining, partial icon override, uniform message, unknown-level rejection, inline icon mapping

## 10. Low-level building blocks

- [x] 10.1 Extract `configure_levels(logger, theme, *, icons=...)` (registers per-level color+icon, adds no sink)
- [x] 10.2 Extract public `build_format(theme, *, icons=...)` and `resolve_icons(theme, spec)`; refactor `apply_theme` to compose them
- [x] 10.3 Tests: configure_levels without sink + own `logger.add`; build_format usable in a custom sink; resolve_icons specs

## 11. ANSI color scheme (native-tag remapping)

- [x] 11.1 Add `AnsiPalette` (16 colors, validated) and optional `Theme.palette`; canonical palettes for all built-ins
- [x] 11.2 `palette.py`: `install_palette`/`restore_palette`/`using_palette`/`palette_active`, patching `loguru._colorizer.AnsiParser` (guarded import)
- [x] 11.3 Wire `remap_colors` into `apply_theme` (default True; restore when theme has no palette; warn-and-skip if loguru internals absent)
- [x] 11.4 Tests: native `<red>` follows palette, background `<GREEN>`, restore brings back standard colors, `remap_colors=False` opt-out

## 12. Docs & demo updates

- [x] 12.1 README: message color, ERROR/CRITICAL highlight, customization, low-level usage, theme-as-color-scheme sections
- [x] 12.2 `main.py`: introspection, custom formatter, native-tags-use-palette demos
