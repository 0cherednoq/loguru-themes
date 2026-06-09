---
title: Справочник API
description: Публичные функции и типы — краткий справочник по использованию.
---

Всё перечисленное импортируется из `loguru_themes`.

## Функции

### `apply_theme(logger, theme, *, icons=True, sink=None, level="TRACE", colorize=None, replace=True, remap_colors=True)`

Настроить `logger` форматом, цветами и иконками темы. Возвращает id обработчика loguru.

- **theme** — имя встроенной темы, имя зарегистрированной темы или `Theme`.
- **icons** — `True` (иконки темы), `False` (без иконок), `IconSet` или словарь
  вида `{"error": "!!"}`.
- **sink** — выходной sink; по умолчанию `sys.stderr`.
- **colorize** — `None` автоопределяет поток; `True`/`False` форсируют.
- **replace** — `True` сначала удаляет существующие обработчики (забрать консоль).
- **remap_colors** — `True` переназначает нативные теги на палитру темы.

### `get_theme(name) -> Theme`

Найти тему по имени (регистронезависимо). `KeyError`, если темы нет.

### `list_themes() -> list[str]`

Все доступные имена тем (встроенные + зарегистрированные), отсортированные.

### `register_theme(theme, *, overwrite=False)`

Зарегистрировать свою `Theme` для поиска/применения по имени. Встроенные имена защищены.

### `configure_levels(logger, theme, *, icons=True) -> Theme`

Зарегистрировать цвет + иконку на уровень в `logger` и **не** добавлять sink.

### `build_format(theme, *, icons=True)`

Вернуть значение `format` для loguru (строку или callable).

### Управление палитрой

- `install_palette(palette)` — переназначить нативные теги loguru на палитру.
- `restore_palette()` — откатить.
- `using_palette(palette)` — контекстный менеджер (восстановление на выходе).
- `palette_active() -> bool`

## Типы

### `Theme`

Поля: `name`, `levels` (`dict[str, LevelStyle]`), `accent`, `dim`, `fg`,
`icons` (`IconSet`), `fmt` (опциональное переопределение формата),
`palette` (`AnsiPalette`).

Неизменяемые хелперы `with_*` (каждый возвращает новую `Theme`): `with_name`,
`with_accent`, `with_dim`, `with_fg`, `with_format`, `with_palette`,
`with_color`, `with_level`, `with_icon`, `with_icons`, `with_uniform_message`.

### `LevelStyle(color, bold=False, bg=None, msg_fg=None, msg_bg=None, msg_bold=False)`

Как выглядит уровень — бейдж (`color`, `bold`, `bg`) и сообщение (`msg_fg`,
`msg_bg`, `msg_bold`). `.markup()` возвращает токен цвета loguru.

### `IconSet(trace, debug, info, success, warning, error, critical)`

Юникод-символы на уровень. `.get(level)` (регистронезависимо) и
`.replace(mapping_or_kwargs)` для частичной замены.

### `AnsiPalette(black, red, green, yellow, blue, magenta, cyan, white, bright_*)`

16 именованных ANSI-цветов для переназначения нативных тегов.

### `ThemeName`

`Literal` с именами встроенных тем — для автодополнения в IDE.

## Константы

- `LEVELS` — семь стандартных имён уровней loguru.
- `DEFAULT_ICONS`, `NO_ICONS` — набор иконок по умолчанию и пустой.
