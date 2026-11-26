"""Lowercase a-z (U+0061-007A)."""
from ..components import arch, frame
from ..config import Params
from ..registry import glyph


@glyph("n", 0x6E, width=lambda p: p.adv(p.lc_w))
def n(p: Params):
    return [arch(p, p.sb, p.sb + p.lc_w, p.xh, outer="tl", inner="tr")]


@glyph("o", 0x6F, width=lambda p: p.adv(p.lc_w))
def o(p: Params):
    return frame(p, p.sb, 0, p.sb + p.lc_w, p.xh, outer="tl", inner="tr")
