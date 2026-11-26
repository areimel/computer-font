"""Sidebearing and space-width rules, all Params-driven so they scale with weight.

Glyphs draw at ``x = p.sb``; this module lets a glyph name a *target* left/right
sidebearing as a multiple of ``p.sb``. ``ufo.py`` then translates the outline so its
ink starts at the target lsb and sets the advance to ink + lsb + rsb. Glyphs not
listed keep their drawn bearings.
"""
from __future__ import annotations

from .config import Params

# group -> (lsb multiple, rsb multiple) of p.sb
_GROUPS: dict[str, tuple[tuple[float, float], str]] = {
    # stems drawn inside a wider box: pull them in, keep a little air
    "stem": ((1.2, 1.2), "i l I bar"),
    "one": ((1.4, 1.4), "one"),
    "j": ((0.8, 1.0), "j"),
    # open diagonals leave air at the top/bottom, so sit closer
    "diag_v": ((0.5, 0.5), "V W Y v w y"),
    "diag_x": ((0.7, 0.7), "X x slash backslash asciicircum"),
    "diag_k": ((1.0, 0.7), "K k Z z"),
    # shapes open on the right (arm or bar overhang)
    "open_r": ((1.0, 0.6), "L F P r f seven"),
    "bar_t": ((0.7, 0.7), "T"),
    "t": ((0.8, 0.8), "t"),
    "dots": ((1.0, 1.0), "period comma colon semicolon exclam quotesingle quotedbl grave"),
}

BEARINGS: dict[str, tuple[float, float]] = {
    name: mult for mult, names in _GROUPS.values() for name in names.split()
}


def bearings(name: str, p: Params) -> tuple[int, int] | None:
    """Target (lsb, rsb) in font units for ``name``, or None to keep drawn bearings."""
    mult = BEARINGS.get(name)
    return None if mult is None else (round(mult[0] * p.sb), round(mult[1] * p.sb))


def space_width(p: Params) -> int:
    """Word space: 0.25 em at the lightest master growing to ~0.29 em at the heaviest."""
    return 170 + 2 * p.sb
