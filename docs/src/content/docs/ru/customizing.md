---
title: Кастомизация
description: Подправить встроенную тему или собрать свою.
---

## Подправить существующую тему

Темы неизменяемы — каждый хелпер `with_*` возвращает **новую** тему, поэтому
вызовы можно объединять в цепочку, а оригинал не меняется:

```python
from loguru import logger
from loguru_themes import apply_theme, get_theme

my_theme = (
    get_theme("dracula")
    .with_name("my-dracula")        # переименовать (например, перед регистрацией)
    .with_color("INFO", "#ffffff")  # цвет одного уровня
    .with_icon("error", "!!")       # иконка одного уровня
    .with_fg("#e6e6e6")             # цвет текста сообщения
)
apply_theme(logger, my_theme)
```

Доступные хелперы: `with_name`, `with_fg`, `with_accent`, `with_dim`,
`with_format`, `with_palette`, `with_color(level, color)`,
`with_level(level, **fields)`, `with_icon(level, icon)`,
`with_icons(set_or_mapping)`, `with_uniform_message(color=...)`.

### Один цвет для всех сообщений

Убрать красную подсветку ERROR / CRITICAL и сделать единый цвет текста:

```python
plain = get_theme("dracula").with_uniform_message("#e6e6e6")
apply_theme(logger, plain)
```

### Перекрасить один уровень

`with_level` задаёт любые поля `LevelStyle` — бейдж (`color`, `bold`, `bg`) и
сообщение (`msg_fg`, `msg_bg`, `msg_bold`):

```python
theme = get_theme("dracula").with_level(
    "WARNING", color="#ffd166", bold=True, msg_fg="#ffd166"
)
```

## Собрать тему с нуля

```python
from loguru_themes import Theme, LevelStyle, register_theme, apply_theme

ocean = Theme(
    name="ocean",
    levels={
        "TRACE":    LevelStyle("#5b7083"),
        "DEBUG":    LevelStyle("#48cae4"),
        "INFO":     LevelStyle("#90e0ef"),
        "SUCCESS":  LevelStyle("#52b788"),
        "WARNING":  LevelStyle("#ffb703"),
        "ERROR":    LevelStyle("#ef476f", msg_fg="#ef476f"),
        "CRITICAL": LevelStyle("#ff5d8f", bold=True,
                               msg_fg="#ffffff", msg_bg="#d00000", msg_bold=True),
    },
    accent="#48cae4",
    dim="#5b7083",
    fg="#caf0f8",
)
register_theme(ocean)
apply_theme(logger, "ocean")
```

Тему можно применить и напрямую, без регистрации: `apply_theme(logger, ocean)`.

### Регистрация

- `register_theme(theme)` делает тему доступной по имени через `apply_theme` /
  `get_theme`.
- Повторная регистрация того же имени требует `overwrite=True`.
- Встроенные имена заменить нельзя.
