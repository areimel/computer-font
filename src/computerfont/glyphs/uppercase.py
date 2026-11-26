"""Uppercase A-Z (U+0041-005A). Rectilinear letters; K N V X Y Z (diagonals) live in uppercase_diag.py."""
from ..components import cap_width, frame, mid_bar, notched_poly, notched_rect
from ..config import Params
from ..geometry import rect
from ..registry import glyph


def _wide_w(p: Params) -> int:
    return p.cap_w + p.stem  # M / W box


def _wide(p: Params) -> int:
    return p.adv(_wide_w(p))


def _narrow(p: Params) -> int:
    return p.adv(p.stem)  # I


def _term(p: Params) -> int:
    """Terminal length of C/G/S/J beyond their horizontal bar."""
    return 2 * p.notch


@glyph("A", 0x41, width=cap_width)
def A(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo = (p.cap - b) // 3
    outer = [(x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap)]
    return [notched_poly(p, outer, tl=(6, 7)), rect(x0 + s, lo + b, x1 - s2, p.cap - b).counter()]


@glyph("B", 0x42, width=cap_width)
def B(p: Params):
    x0, x1, s, s2, b, n = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, p.notch
    ym = p.cap // 2
    lo, hi = mid_bar(p)
    outer = [
        (x0, 0), (x1, 0), (x1, ym - n), (x1 - n, ym - n), (x1 - n, ym + n), (x1, ym + n), (x1, p.cap), (x0, p.cap)
    ]
    return [
        notched_poly(p, outer, tl=7),
        rect(x0 + s, b, x1 - s2, lo).counter(),
        rect(x0 + s, hi, x1 - s2, p.cap - b).counter(),
    ]


@glyph("C", 0x43, width=cap_width)
def C(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    c = [
        (x0, 0), (x1, 0), (x1, b + t), (x1 - s2, b + t), (x1 - s2, b), (x0 + s, b), (x0 + s, p.cap - b),
        (x1 - s2, p.cap - b), (x1 - s2, p.cap - b - t), (x1, p.cap - b - t), (x1, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=11)]


@glyph("D", 0x44, width=cap_width)
def D(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl tr br")


@glyph("E", 0x45, width=cap_width)
def E(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    lo, hi = mid_bar(p)
    xm = x1 - s
    c = [
        (x0, 0), (x1, 0), (x1, b), (x0 + s, b), (x0 + s, lo), (xm, lo), (xm, hi), (x0 + s, hi),
        (x0 + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=11)]


@glyph("F", 0x46, width=cap_width)
def F(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    lo, hi = mid_bar(p)
    xm = x1 - s
    c = [
        (x0, 0), (x0 + s, 0), (x0 + s, lo), (xm, lo), (xm, hi), (x0 + s, hi),
        (x0 + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=9)]


@glyph("G", 0x47, width=cap_width)
def G(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    yg = mid_bar(p)[1]
    xg = (x0 + x1) // 2
    c = [
        (x0, 0), (x1, 0), (x1, yg), (xg, yg), (xg, yg - b), (x1 - s2, yg - b), (x1 - s2, b), (x0 + s, b),
        (x0 + s, p.cap - b), (x1 - s2, p.cap - b), (x1 - s2, p.cap - b - t), (x1, p.cap - b - t),
        (x1, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=13)]


@glyph("H", 0x48, width=cap_width)
def H(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    lo, hi = mid_bar(p)
    c = [
        (x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0),
        (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, hi), (x0 + s, hi), (x0 + s, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=11)]


@glyph("I", 0x49, width=_narrow)
def I(p: Params):
    return [notched_rect(p, p.sb, 0, p.sb + p.stem, p.cap, "tl")]


@glyph("J", 0x4A, width=cap_width)
def J(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    c = [
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s, p.cap), (x1 - s, b), (x0 + s2, b), (x0 + s2, b + t), (x0, b + t)
    ]
    return [notched_poly(p, c, tl=3)]


@glyph("L", 0x4C, width=cap_width)
def L(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    return [notched_poly(p, [(x0, 0), (x1, 0), (x1, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap)], tl=5)]


@glyph("M", 0x4D, width=_wide)
def M(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + _wide_w(p), p.stem, p.stem2, p.bar
    m0 = (x0 + x1 - s2) // 2
    c = [
        (x0, 0), (x0 + s, 0), (x0 + s, p.cap - b), (m0, p.cap - b), (m0, 0), (m0 + s2, 0), (m0 + s2, p.cap - b),
        (x1 - s2, p.cap - b), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=11)]


@glyph("O", 0x4F, width=cap_width)
def O(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl", inner="tr")


@glyph("P", 0x50, width=cap_width)
def P(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo, hi = mid_bar(p)
    outer = [(x0, 0), (x0 + s, 0), (x0 + s, lo), (x1, lo), (x1, p.cap), (x0, p.cap)]
    return [notched_poly(p, outer, tl=5), rect(x0 + s, hi, x1 - s2, p.cap - b).counter()]


@glyph("Q", 0x51, width=cap_width)
def Q(p: Params):
    x1 = p.sb + p.cap_w
    tail = rect(x1 - 2 * p.stem2, -2 * p.notch, x1, p.bar)
    return [*frame(p, p.sb, 0, x1, p.cap, outer="tl", inner="tr"), tail]


@glyph("R", 0x52, width=cap_width)
def R(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo, hi = mid_bar(p)
    outer = [(x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap)]
    return [notched_poly(p, outer, tl=(7, 5)), rect(x0 + s, hi, x1 - s2, p.cap - b).counter()]


@glyph("S", 0x53, width=cap_width)
def S(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    lo, hi = mid_bar(p)
    c = [
        (x0, 0), (x1, 0), (x1, hi), (x0 + s, hi), (x0 + s, p.cap - b), (x1 - s2, p.cap - b),
        (x1 - s2, p.cap - b - t), (x1, p.cap - b - t), (x1, p.cap), (x0, p.cap), (x0, lo),
        (x1 - s2, lo), (x1 - s2, b), (x0 + s, b), (x0 + s, b + t), (x0, b + t),
    ]
    return [notched_poly(p, c, tl=9)]


@glyph("T", 0x54, width=cap_width)
def T(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    cx = (x0 + x1 - s) // 2
    c = [
        (cx, 0), (cx + s, 0), (cx + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap), (x0, p.cap - b),
        (cx, p.cap - b),
    ]
    return [notched_poly(p, c, tl=5)]


@glyph("U", 0x55, width=cap_width)
def U(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    c = [
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap)
    ]
    return [notched_poly(p, c, tl=7)]


@glyph("W", 0x57, width=_wide)
def W(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + _wide_w(p), p.stem, p.stem2, p.bar
    m0 = (x0 + x1 - s2) // 2
    top = p.cap - p.cap // 4
    c = [
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, b), (m0 + s2, b), (m0 + s2, top), (m0, top),
        (m0, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap),
    ]
    return [notched_poly(p, c, tl=11)]
