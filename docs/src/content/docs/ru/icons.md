---
title: Иконки
description: Юникод-иконки уровней — отключить, заменить или переопределить на месте.
---

Каждая тема рисует минималистичную юникод-иконку рядом с уровнем. По умолчанию
(спец-шрифты не нужны):

| Уровень  | Иконка |
| -------- | ------ |
| TRACE    | `›`    |
| DEBUG    | `•`    |
| INFO     | `•`    |
| SUCCESS  | `✔`    |
| WARNING  | `!`    |
| ERROR    | `✖`    |
| CRITICAL | `✖`    |

## Отключить иконки

```python
apply_theme(logger, "dracula", icons=False)
```

Выравнивание сохраняется — пустого места от иконки не остаётся.

## Переопределить часть иконок на месте

Передай словарь, чтобы поменять только нужные уровни; остальные сохранят иконки темы:

```python
apply_theme(logger, "dracula", icons={"error": "💥", "info": "i"})
```

## Полный свой набор иконок

```python
from loguru_themes import IconSet, apply_theme

arrows = IconSet(
    trace="→", debug="→", info="→", success="✓",
    warning="▲", error="✕", critical="✕",
)
apply_theme(logger, "dracula", icons=arrows)
```

## На уровне темы

Изменения иконок можно «вшить» в тему (см. [Кастомизацию](../customizing/)):

```python
from loguru_themes import get_theme, apply_theme

theme = get_theme("dracula").with_icon("error", "!!")
apply_theme(logger, theme)
```
