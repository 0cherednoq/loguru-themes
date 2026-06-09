"""01 — Quickstart: apply a theme in one line.

Run:  python examples/01_quickstart.py
"""

from loguru import logger

from loguru_themes import apply_theme

# One call configures the console sink: format, per-level colors, and icons.
apply_theme(logger, "dracula")

logger.trace("entering low-level routine")
logger.debug("resolved config from environment")
logger.info("server listening on http://localhost:8000")
logger.success("migration completed in 1.2s")
logger.warning("cache miss rate above 30%")
logger.error("failed to reach upstream service")     # red message text
logger.critical("data corruption detected — aborting")  # bold on red background
