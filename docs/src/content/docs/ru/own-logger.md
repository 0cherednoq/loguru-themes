---
title: Свой логгер
description: Использовать свои sink-и и формат через строительные блоки темы.
---

`apply_theme` удобен, но забирает управление логгером. Когда нужны свои sink-и
или формат, используй строительные блоки, из которых он собран.

## `configure_levels` — цвета и иконки, без sink

Регистрирует цвет и иконку темы для каждого уровня (через `logger.level(...)`) и
**не** добавляет sink. В своём формате ссылайся на `<level>` и `{level.icon}`:

```python
import sys
from loguru import logger
from loguru_themes import configure_levels

logger.remove()
configure_levels(logger, "dracula")           # цвета + иконки, без sink
logger.add(
    sys.stderr,
    format="<level>{level.icon} {level.name}</level> | {message}",
    colorize=True,
)
```

## `build_format` — значение формата темы

Отдаёт значение `format` для loguru (строку или callable для тем с подсветкой
сообщений) для твоего `logger.add(...)`:

```python
from loguru_themes import configure_levels, build_format

configure_levels(logger, "dracula")
logger.add("app.log", format=build_format("dracula"), colorize=True, rotation="10 MB")
```

## Ссылаться на цвета темы в своём формате

Hex хардкодить не нужно — бери его из темы. `<level>` автоматически использует
цвет текущего уровня; для фиксированных частей подставляй `theme.accent` /
`dim` / `fg`:

```python
from loguru_themes import get_theme, configure_levels

theme = get_theme("dracula")
fmt = (
    f"<fg {theme.accent}>┃</>"
    f" <fg {theme.dim}>{{time:HH:mm:ss}}</>"
    f" <level>{{level.icon}} {{level.name: <8}}</level>"
    f" <fg {theme.fg}>{{message}}</>"
)
configure_levels(logger, theme)
logger.add(sys.stderr, format=fmt, colorize=True, level="TRACE")
```

Сырой токен цвета одного уровня: `theme.levels["ERROR"].markup()` → `'<fg #ff5555>'`.

## Консоль + файл

`colorize=None` (по умолчанию) автоопределяет поток: цвет в терминале, чистый
текст в файле — без сырых тегов разметки.

```python
configure_levels(logger, "dracula")
fmt = build_format("dracula")
logger.add(sys.stderr, format=fmt, colorize=True)    # цветная консоль
logger.add("app.log", format=fmt, colorize=False)    # чистый файл
```
