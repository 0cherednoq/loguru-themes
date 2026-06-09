"""Tests for loguru_themes: model validation, registry, apply, icons, fallback."""

from __future__ import annotations

import io
import re

import pytest
from loguru import logger

from loguru_themes import (
    DEFAULT_ICONS,
    IconSet,
    LevelStyle,
    Theme,
    apply_theme,
    build_format,
    configure_levels,
    get_theme,
    install_palette,
    list_themes,
    palette_active,
    register_theme,
    resolve_icons,
    restore_palette,
)
from loguru_themes.registry import _reset_custom_themes

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
MARKUP_RE = re.compile(r"</?(level|fg|bold|dim)\b|</>")


def ansi_fg(hex_color: str) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"38;2;{r};{g};{b}"


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


@pytest.fixture(autouse=True)
def clean_state():
    """Reset custom themes and logger handlers around each test."""
    _reset_custom_themes()
    restore_palette()
    logger.remove()
    yield
    _reset_custom_themes()
    restore_palette()
    logger.remove()


def _full_levels() -> dict[str, LevelStyle]:
    return {lvl: LevelStyle("#888888") for lvl in
            ("TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL")}


# --- 7.1 model validation + registry -------------------------------------

def test_theme_missing_level_rejected():
    levels = _full_levels()
    del levels["WARNING"]
    with pytest.raises(ValueError) as exc:
        Theme(name="broken", levels=levels, accent="#000000", dim="#111111")
    assert "WARNING" in str(exc.value)


def test_theme_invalid_hex_rejected():
    with pytest.raises(ValueError):
        LevelStyle("not-a-color")


def test_get_theme_case_insensitive():
    assert get_theme("dracula") is get_theme("DRACULA")
    assert get_theme("Dracula").name == "dracula"


def test_unknown_theme_lists_available():
    with pytest.raises(KeyError) as exc:
        get_theme("does-not-exist")
    msg = str(exc.value)
    for name in ("dracula", "nord", "catppuccin", "monokai", "dark", "light"):
        assert name in msg


def test_list_themes_contains_all_builtins():
    names = list_themes()
    for name in ("dracula", "nord", "catppuccin", "monokai", "dark", "light"):
        assert name in names


def test_theme_name_literal_matches_builtins():
    # The ThemeName Literal (for IDE autocomplete) must stay in sync with the
    # actual built-in themes.
    import typing

    from loguru_themes import ThemeName
    from loguru_themes.themes import BUILTIN_THEMES

    assert set(typing.get_args(ThemeName)) == set(BUILTIN_THEMES)


def test_register_and_apply_custom_theme():
    theme = Theme(name="my-theme", levels=_full_levels(),
                  accent="#abcdef", dim="#123456")
    register_theme(theme)
    assert "my-theme" in list_themes()
    buf = io.StringIO()
    apply_theme(logger, "my-theme", sink=buf, colorize=True)
    logger.info("hi")
    assert "hi" in strip_ansi(buf.getvalue())


def test_register_cannot_override_builtin():
    theme = Theme(name="dracula", levels=_full_levels(),
                  accent="#abcdef", dim="#123456")
    with pytest.raises(ValueError):
        register_theme(theme)


def test_register_duplicate_requires_overwrite():
    t1 = Theme(name="dup", levels=_full_levels(), accent="#aaaaaa", dim="#bbbbbb")
    register_theme(t1)
    with pytest.raises(ValueError):
        register_theme(t1)
    register_theme(t1, overwrite=True)  # ok


# --- 7.2 apply idempotency + distinct colors ------------------------------

def test_apply_is_idempotent():
    buf = io.StringIO()
    apply_theme(logger, "dracula", sink=buf, colorize=True)
    apply_theme(logger, "dracula", sink=buf, colorize=True)
    logger.info("only once")
    lines = [ln for ln in strip_ansi(buf.getvalue()).splitlines() if "only once" in ln]
    assert len(lines) == 1


def test_each_level_has_distinct_color():
    buf = io.StringIO()
    theme = get_theme("dracula")
    apply_theme(logger, theme, sink=buf, colorize=True)
    for lvl in ("info", "warning", "error"):
        getattr(logger, lvl)(f"msg-{lvl}")
    out = buf.getvalue()
    for lvl in ("INFO", "WARNING", "ERROR"):
        assert ansi_fg(theme.levels[lvl].color) in out
    # colors really differ
    assert theme.levels["INFO"].color != theme.levels["ERROR"].color


# --- 7.3 icons render / override / disable --------------------------------

def test_icon_appears_and_matches_level_color():
    buf = io.StringIO()
    theme = get_theme("dracula")
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.success("done")
    success_line = next(
        ln for ln in buf.getvalue().splitlines() if "done" in ln
    )
    assert DEFAULT_ICONS.success in success_line
    # icon shares the success color: the color code appears before the icon
    color = ansi_fg(theme.levels["SUCCESS"].color)
    idx_color = success_line.index(color)
    idx_icon = success_line.index(DEFAULT_ICONS.success)
    assert idx_color < idx_icon


def test_custom_icon_set_overrides():
    buf = io.StringIO()
    arrows = IconSet(trace="→", debug="→", info="→", success="✓",
                     warning="▲", error="✕", critical="✕")
    apply_theme(logger, "dracula", icons=arrows, sink=buf, colorize=True)
    logger.success("done")
    out = buf.getvalue()
    assert "✓" in out
    assert DEFAULT_ICONS.success not in out  # default ✔ replaced


def test_disabled_icons_leave_no_stray_markup():
    buf = io.StringIO()
    apply_theme(logger, "dracula", icons=False, sink=buf, colorize=True)
    logger.info("clean")
    out = buf.getvalue()
    # no default icons present
    for icon in (DEFAULT_ICONS.success, DEFAULT_ICONS.error, DEFAULT_ICONS.trace):
        assert icon not in out
    # no raw markup / no empty icon placeholder
    assert not MARKUP_RE.search(out)
    assert "{level.icon}" not in out
    # level name still rendered and aligned
    assert "INFO" in strip_ansi(out)


def test_error_message_is_red_foreground_no_background():
    buf = io.StringIO()
    theme = get_theme("dracula")
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.error("boom")
    error_line = next(ln for ln in buf.getvalue().splitlines() if "boom" in ln)
    assert theme.levels["ERROR"].msg_bg is None
    assert ansi_fg(theme.levels["ERROR"].msg_fg) in error_line  # red text
    assert "48;2;" not in error_line  # no background SGR on the line


def test_critical_message_has_background():
    buf = io.StringIO()
    theme = get_theme("dracula")
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.critical("doom")
    crit_line = next(ln for ln in buf.getvalue().splitlines() if "doom" in ln)
    bg = theme.levels["CRITICAL"].msg_bg
    r, g, b = (int(bg[i:i + 2], 16) for i in (1, 3, 5))
    assert f"48;2;{r};{g};{b}" in crit_line  # background SGR on the message


def test_exception_traceback_still_renders():
    buf = io.StringIO()
    apply_theme(logger, "dracula", sink=buf, colorize=False)
    try:
        raise ValueError("kaboom")
    except ValueError:
        logger.exception("operation failed")
    out = buf.getvalue()
    assert "operation failed" in out
    assert "Traceback (most recent call last):" in out
    assert "ValueError: kaboom" in out
    # message line is not blank-duplicated
    assert sum("operation failed" in ln for ln in out.splitlines()) == 1


# --- customization API ----------------------------------------------------

def test_with_helpers_are_immutable_and_chain():
    base = get_theme("dracula")
    custom = (
        base.with_name("my-dracula")
        .with_color("INFO", "#ffffff")
        .with_icon("error", "!!")
        .with_fg("#eeeeee")
    )
    # original untouched
    assert base.name == "dracula"
    assert base.levels["INFO"].color != "#ffffff"
    assert base.icons.error != "!!"
    # copy carries the overrides
    assert custom.name == "my-dracula"
    assert custom.levels["INFO"].color == "#ffffff"
    assert custom.icons.error == "!!"
    assert custom.fg == "#eeeeee"


def test_with_icons_mapping_partial_override():
    theme = get_theme("dracula").with_icons({"warning": "▲", "ERROR": "x"})
    assert theme.icons.warning == "▲"
    assert theme.icons.error == "x"
    assert theme.icons.info == get_theme("dracula").icons.info  # others kept


def test_with_uniform_message_clears_highlights():
    theme = get_theme("dracula").with_uniform_message("#cccccc")
    for style in theme.levels.values():
        assert style.msg_fg is None
        assert style.msg_bg is None
        assert style.msg_bold is False
    assert theme.fg == "#cccccc"
    # applied output: ERROR message is no longer red, just the uniform fg
    buf = io.StringIO()
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.error("boom")
    line = next(ln for ln in buf.getvalue().splitlines() if "boom" in ln)
    assert ansi_fg("#cccccc") in line
    assert "48;2;" not in line


def test_with_level_rejects_unknown_level():
    with pytest.raises(KeyError):
        get_theme("dracula").with_level("FATAL", color="#000000")


def test_apply_theme_icons_mapping_override():
    buf = io.StringIO()
    apply_theme(logger, "dracula", icons={"info": ">>"}, sink=buf, colorize=True)
    logger.info("hello")
    assert ">>" in buf.getvalue()


def test_unknown_icon_level_rejected():
    with pytest.raises(KeyError):
        get_theme("dracula").with_icon("fatal", "x")


# --- low-level building blocks --------------------------------------------

def test_configure_levels_without_sink_then_own_add():
    # configure_levels adds NO sink; user wires their own logger.add().
    configure_levels(logger, "dracula")
    assert logger._core.handlers == {}  # nothing added yet
    buf = io.StringIO()
    logger.add(buf, format="<level>{level.icon} {level.name}</level> {message}",
               colorize=True)
    logger.error("custom wiring")
    out = buf.getvalue()
    assert DEFAULT_ICONS.error in out  # icon picked up from configure_levels
    assert ansi_fg(get_theme("dracula").levels["ERROR"].color) in out  # color too


def test_build_format_returns_usable_value():
    # neutral theme -> string; dracula (highlights) -> callable.
    plain = get_theme("dracula").with_uniform_message()
    assert isinstance(build_format(plain), str)
    assert callable(build_format("dracula"))
    # the format value works in a hand-rolled logger.add()
    buf = io.StringIO()
    logger.remove()
    configure_levels(logger, "dracula")
    logger.add(buf, format=build_format("dracula"), colorize=True)
    logger.info("manual")
    assert "manual" in strip_ansi(buf.getvalue())


def test_resolve_icons_spec():
    theme = get_theme("dracula")
    iset, enabled = resolve_icons(theme, True)
    assert enabled and iset is theme.icons
    iset, enabled = resolve_icons(theme, False)
    assert not enabled and iset.error == ""
    iset, enabled = resolve_icons(theme, {"error": "!!"})
    assert enabled and iset.error == "!!" and iset.info == theme.icons.info


# --- ANSI palette remapping (theme as a real color scheme) ----------------

def test_named_tags_remapped_to_theme_palette():
    theme = get_theme("dracula")
    buf = io.StringIO()
    # apply_theme installs the palette by default; write a native <red> tag.
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.opt(colors=True).info("<red>danger</red>")
    out = buf.getvalue()
    assert ansi_fg(theme.palette.red) in out          # dracula red, truecolor
    assert "\x1b[31m" not in out                       # not standard ANSI red


def test_restore_palette_brings_back_standard_colors():
    install_palette(get_theme("dracula").palette)
    assert palette_active()
    restore_palette()
    assert not palette_active()
    buf = io.StringIO()
    logger.add(buf, format="<red>{message}</red>", colorize=True)
    logger.info("x")
    assert "\x1b[31m" in buf.getvalue()                # standard red is back


def test_remap_colors_false_leaves_loguru_defaults():
    buf = io.StringIO()
    apply_theme(logger, "dracula", sink=buf, colorize=True, remap_colors=False)
    assert not palette_active()
    logger.opt(colors=True).info("<red>danger</red>")
    assert "\x1b[31m" in buf.getvalue()                # standard red, not remapped


def test_background_tag_remapped():
    theme = get_theme("dracula")
    buf = io.StringIO()
    apply_theme(logger, theme, sink=buf, colorize=True)
    logger.opt(colors=True).info("<GREEN>ok</GREEN>")
    r, g, b = (int(theme.palette.green[i:i + 2], 16) for i in (1, 3, 5))
    assert f"48;2;{r};{g};{b}" in buf.getvalue()        # theme green as background


# --- 7.4 no-color fallback ------------------------------------------------

def test_no_color_stream_has_no_markup_or_ansi():
    buf = io.StringIO()
    apply_theme(logger, "dracula", sink=buf, colorize=False)
    for lvl in ("info", "warning", "error", "critical"):
        getattr(logger, lvl)(f"plain-{lvl}")
    out = buf.getvalue()
    assert "\x1b[" not in out  # no ANSI escapes
    assert not MARKUP_RE.search(out)  # no raw markup tags
    assert "plain-info" in out
