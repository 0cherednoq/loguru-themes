---
title: Цветовая схема
description: Нативные цветовые теги loguru следуют палитре темы.
---

Тема — это не просто пара акцентных цветов: она несёт полную 16-цветную
ANSI-палитру. При применении темы **нативные цветовые теги** loguru
переназначаются на палитру темы — как цветовая схема терминала.

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "dracula")
logger.opt(colors=True).info("<red>danger</red> <blue>info</blue> <green>ok</green>")
# <red>/<blue>/<green> рендерятся в цветах Dracula. Сменишь на "monokai" — те же
# теги изменятся соответственно.
```

Это работает для нативных тегов в **строках формата** и в сообщениях
`logger.opt(colors=True)`:

- передний план: `<red>`, короткое `<r>`, яркое `<light-red>` …
- фон: `<RED>`, короткое `<R>` …
- альтернативный синтаксис `<fg name>` / `<bg name>`

## Текст и фон

Строчные теги красят **текст**, ЗАГЛАВНЫЕ — **фон**. Тег фона сам по себе не
меняет цвет текста, поэтому для читаемости задавай ещё и передний план:

```python
logger.opt(colors=True).info("<black><GREEN> OK </GREEN></black>")
logger.opt(colors=True).info("<white><RED> ERROR </RED></white>")
```

## Управление и область действия

Переназначение глобально на процесс (так и работает цветовая схема).

```python
# Не трогать стандартные цвета loguru:
apply_theme(logger, "dracula", remap_colors=False)

# Откатить вручную:
from loguru_themes import restore_palette
restore_palette()

# Ограничить блоком (восстановится на выходе):
from loguru_themes import using_palette, get_theme
with using_palette(get_theme("nord").palette):
    logger.opt(colors=True).info("<red>здесь красный из Nord</red>")
```

Палитра доступна как `theme.palette` (объект `AnsiPalette`); задать свою —
`theme.with_palette(AnsiPalette(...))`.
