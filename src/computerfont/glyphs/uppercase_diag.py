"""Uppercase letters built on straight diagonals: K N V X Y Z.

Every diagonal is a parallelogram/polygon with a fixed vertex count; only the
coordinates (derived from ``Params``) change with weight, so masters stay compatible.
"""
from ..components import cap_width, notched_rect
from ..config import Params
from ..geometry import polygon, rect
from ..registry import glyph


def _vee_poly(x0: float, x1: float, y0: float, y1: float, sl: float, sr: float, hw: float) -> list:
    """Points (CCW) of a V from bottom-flat at y0 to the top at y1, left arm sl wide, right sr wide.

    Bottom flat (half-width ``hw``) is centred; both arms keep the slope of their outer edges.
    """
    cx = (x0 + x1) / 2
    a, b = cx - hw, x1 - cx - hw  # horizontal run of left/right outer edge
    t = (x1 - sr - x0 - sl) / (a + b)
    iy = y1 - (y1 - y0) * t
    ix = x0 + sl + t * a
    return [(cx - hw, y0), (cx + hw, y0), (x1, y1), (x1 - sr, y1), (ix, iy), (x0 + sl, y1), (x0, y1)]


@glyph("V", 0x56, width=cap_width)
def V(p: Params):
    return [polygon(*_vee_poly(p.sb, p.sb + p.cap_w, 0, p.cap, p.stem, p.stem2, (p.stem + p.stem2) / 3))]


@glyph("Y", 0x59, width=cap_width)
def Y(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    ym = p.cap * 2 // 5
    hw = (s + s2) / 4  # half stalk
    cx = (x0 + x1) / 2
    top = _vee_poly(x0, x1, ym, p.cap, s, s2, hw)
    return [polygon((cx - hw, 0), (cx + hw, 0), *top[1:], (cx - hw, ym))]


@glyph("X", 0x58, width=cap_width)
def X(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    return [
        polygon((x0, 0), (x0 + s2, 0), (x1, p.cap), (x1 - s2, p.cap)),
        polygon((x1 - s, 0), (x1, 0), (x0 + s, p.cap), (x0, p.cap)),
    ]


@glyph("K", 0x4B, width=cap_width)
def K(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    yj = p.cap // 2 - b // 2  # lower edge of the upper arm's foot
    upper = polygon((x0 + s // 2, yj), (x0 + s + s2, yj), (x1, p.cap), (x1 - s2, p.cap))
    return [notched_rect(p, x0, 0, x0 + s, p.cap, "tl"), upper, upper.flipped(p.cap // 2)]


@glyph("N", 0x4E, width=cap_width)
def N(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    w = s2
    diag = polygon((x0 + s // 2, p.cap), (x0 + s + w, p.cap), (x1 - s2 // 2, 0), (x1 - s2 - w, 0))
    return [notched_rect(p, x0, 0, x0 + s, p.cap, "tl"), rect(x1 - s2, 0, x1, p.cap), diag]


@glyph("Z", 0x5A, width=cap_width)
def Z(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    w = s
    diag = polygon((x0, b // 2), (x0 + w, b // 2), (x1, p.cap - b // 2), (x1 - w, p.cap - b // 2))
    return [notched_rect(p, x0, p.cap - b, x1, p.cap, "tl"), rect(x0, 0, x1, b), diag]
