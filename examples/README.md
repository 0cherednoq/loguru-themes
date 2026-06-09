# Examples

Runnable examples for `loguru_themes`, one file per use case.

## Setup

From the project root, install the package (editable is fine):

```bash
pip install -e .
```

Then run any example:

```bash
python examples/01_quickstart.py
```

> Tip: force colors on when piping output, e.g. set the env var loguru honors,
> or just run in a real terminal. By default color auto-detects the stream.

## Index

| File | Use case |
|------|----------|
| `01_quickstart.py` | Apply a theme in one line; all log levels. |
| `02_customize.py` | Tweak a theme with the immutable `with_*` API (colors, icons, uniform message). |
| `03_color_scheme.py` | Native loguru tags (`<red>`, `<blue>`, …) follow the theme palette; opt-out and scoped use. |

More usage patterns (icons, custom themes, your own sinks/format, file logging)
are covered in the [documentation](../docs/).
