"""Digits 0-9 (U+0030-0039). Boxes are p.lc_w wide, cap height tall."""
from ..components import frame
from ..config import Params
from ..geometry import Contour, Pt, notch_corners
from ..registry import glyph

_NAMES = "zero one two three four five six seven eight nine".split()


def _box(p: Params):
    """Shared digit geometry: x0, x1, mid-bar bottom/top (lo, hi)."""
    x0, x1 = p.sb, p.sb + p.lc_w
    lo = (p.cap - p.bar) // 2
    return x0, x1, lo, lo + p.bar


def _poly(p: Params, pts: list[tuple[float, float]], tl: int | None = None) -> Contour:
    """Orthogonal polygon (CCW input) with the signature square step at vertex ``tl``."""
    c = Contour(tuple(Pt(*q) for q in pts))
    return notch_corners(c, {tl: p.notch}) if tl is not None else c


def _width(p: Params) -> int:
    return p.adv(p.lc_w)


@glyph("zero", 0x30, width=_width)
def zero(p: Params):
    x0, x1, lo, hi = _box(p)
    return frame(p, x0, 0, x1, p.cap, outer="tl", inner="tr")


@glyph("one", 0x31, width=_width)
def one(p: Params):
    x0, x1, lo, hi = _box(p)
    xs = (x0 + x1 - p.stem) / 2 + p.stem / 2  # stem shifted right of centre to make room for the flag
    return [_poly(p, [(xs, 0), (xs + p.stem, 0), (xs + p.stem, p.cap), (xs - p.stem, p.cap),
                      (xs - p.stem, p.cap - p.bar), (xs, p.cap - p.bar)], tl=3)]


@glyph("two", 0x32, width=_width)
def two(p: Params):
    x0, x1, lo, hi = _box(p)
    s, s2, b, c = p.stem, p.stem2, p.bar, p.cap
    return [_poly(p, [(x0, 0), (x1, 0), (x1, b), (x0 + s, b), (x0 + s, lo), (x1, lo), (x1, c), (x0, c),
                      (x0, c - b), (x1 - s2, c - b), (x1 - s2, hi), (x0, hi)], tl=7)]


@glyph("three", 0x33, width=_width)
def three(p: Params):
    x0, x1, lo, hi = _box(p)
    s, s2, b, c = p.stem, p.stem2, p.bar, p.cap
    return [_poly(p, [(x0, 0), (x1, 0), (x1, c), (x0, c), (x0, c - b), (x1 - s2, c - b), (x1 - s2, hi),
                      (x0 + s, hi), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, b), (x0, b)], tl=3)]


@glyph("four", 0x34, width=_width)
def four(p: Params):
    x0, x1, lo, hi = _box(p)
    s, s2, c = p.stem, p.stem2, p.cap
    return [_poly(p, [(x1 - s2, 0), (x1, 0), (x1, c), (x1 - s2, c), (x1 - s2, hi), (x0 + s, hi),
                      (x0 + s, c), (x0, c), (x0, lo), (x1 - s2, lo)], tl=7)]


@glyph("five", 0x35, width=_width)
def five(p: Params):
    x0, x1, lo, hi = _box(p)
    s, s2, b, c = p.stem, p.stem2, p.bar, p.cap
    return [_poly(p, [(x0, 0), (x1, 0), (x1, hi), (x0 + s, hi), (x0 + s, c - b), (x1, c - b), (x1, c),
                      (x0, c), (x0, lo), (x1 - s2, lo), (x1 - s2, b), (x0, b)], tl=7)]


@glyph("six", 0x36, width=_width)
def six(p: Params):
    x0, x1, lo, hi = _box(p)
    s, b, c = p.stem, p.bar, p.cap
    top = _poly(p, [(x0, lo), (x0 + s, lo), (x0 + s, c - b), (x1, c - b), (x1, c), (x0, c)], tl=5)
    return [top, *frame(p, x0, 0, x1, hi)]


@glyph("seven", 0x37, width=_width)
def seven(p: Params):
    x0, x1, lo, hi = _box(p)
    s, s2, b, c = p.stem, p.stem2, p.bar, p.cap
    return [_poly(p, [(x1 - s2, 0), (x1, 0), (x1, c), (x0, c), (x0, c - 2 * b), (x0 + s, c - 2 * b),
                      (x0 + s, c - b), (x1 - s2, c - b)], tl=3)]


@glyph("eight", 0x38, width=_width)
def eight(p: Params):
    x0, x1, lo, hi = _box(p)
    return [*frame(p, x0, lo, x1, p.cap, outer="tl", inner="tr"), *frame(p, x0, 0, x1, hi)]


@glyph("nine", 0x39, width=_width)
def nine(p: Params):
    x0, x1, lo, hi = _box(p)
    s2, b = p.stem2, p.bar
    tail = _poly(p, [(x0, 0), (x1, 0), (x1, hi), (x1 - s2, hi), (x1 - s2, b), (x0, b)])
    return [*frame(p, x0, lo, x1, p.cap, outer="tl", inner="tr"), tail]
