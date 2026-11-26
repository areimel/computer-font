"""Required glyphs: .notdef and space."""
from ..components import frame
from ..config import Params
from ..registry import glyph


@glyph(".notdef", None, width=lambda p: p.adv(p.cap_w))
def notdef(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap)


@glyph("space", 0x20, width=lambda p: 300)
def space(p: Params):
    return []
