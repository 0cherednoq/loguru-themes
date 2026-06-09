---
title: Начало
description: Установка loguru-themes и применение первой темы.
---

## Установка

```bash
pip install loguru-themes
```

Требуется Python 3.9+ и `loguru>=0.7` (ставится автоматически).

## Применение темы

Один вызов настраивает консольный sink — формат, цвета уровней и иконки:

```python
from loguru import logger
from loguru_themes import apply_theme

apply_theme(logger, "dracula")

logger.trace("entering low-level routine")
logger.debug("resolved config from environment")
logger.info("server listening on http://localhost:8000")
logger.success("migration completed in 1.2s")
logger.warning("cache miss rate above 30%")
logger.error("failed to reach upstream service")     # красный текст сообщения
logger.critical("data corruption detected — aborting")  # жирный на красном фоне
```

`apply_theme` берёт на себя консольный вывод логгера (удаляет существующие
обработчики — идиоматичная настройка loguru) и ставит один тематический sink.
Каждый уровень получает свой цвет, а иконка уровня окрашивается в тот же цвет.

![вывод темы dracula](../../../assets/themes/dracula.svg)

## Выбор темы

Передавай имя встроенной темы (IDE подскажет) или объект `Theme`:

```python
apply_theme(logger, "nord")
apply_theme(logger, "catppuccin")
```

Полный список — в разделе [Темы](../themes/), а как подправить — в
[Кастомизации](../customizing/).

## Что дальше

- [Темы](../themes/) — встроенные палитры и как их получить списком
- [Иконки](../icons/) — заменить или отключить иконки уровней
- [Кастомизация](../customizing/) — собрать свою тему
- [Цветовая схема](../color-scheme/) — нативные теги следуют теме
- [Свой логгер](../own-logger/) — использовать свои sink-и и формат
