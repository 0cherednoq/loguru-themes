---
title: Examples
description: Runnable example scripts, one per use case.
---

Runnable scripts live in the `examples/` folder of the repository, one per use
case. From the project root:

```bash
pip install -e .
python examples/01_quickstart.py
```

| File                  | Use case                                                       |
| --------------------- | -------------------------------------------------------------- |
| `01_quickstart.py`    | Apply a theme in one line; all log levels.                     |
| `02_customize.py`     | Tweak a theme with the immutable `with_*` API.                 |
| `03_color_scheme.py`  | Native tags follow the theme palette; opt-out and scoped use.  |

The rest of the use cases — icons, custom themes, your own sinks/format, file
logging — are covered across the guides in this documentation.
