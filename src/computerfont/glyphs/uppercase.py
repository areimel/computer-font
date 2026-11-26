"""Uppercase A-Z (U+0041-005A)."""
from ..components import frame
from ..config import Params
from ..geometry import notch_corners, polygon
from ..registry import glyph


@glyph("H", 0x48, width=lambda p: p.adv(p.cap_w))
def H(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    lo = (p.cap - p.bar) // 2
    hi = lo + p.bar
    c = polygon(
        (x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0),
        (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, hi), (x0 + s, hi), (x0 + s, p.cap), (x0, p.cap),
    )
    return [notch_corners(c, {11: p.notch})]  # step on the top-left corner


@glyph("O", 0x4F, width=lambda p: p.adv(p.cap_w))
def O(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl", inner="tr")
