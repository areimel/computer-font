"""Uppercase A-Z (U+0041-005A). Rectilinear: diagonals are stair-step strokes."""
from ..components import arch, frame, notched_rect
from ..config import Params
from ..geometry import Contour, notch_corners, polygon, rect
from ..registry import glyph


def _cap(p: Params) -> int:
    return p.adv(p.cap_w)


def _wide_w(p: Params) -> int:
    return p.cap_w + p.stem  # M / W box


def _wide(p: Params) -> int:
    return p.adv(_wide_w(p))


def _narrow(p: Params) -> int:
    return p.adv(p.stem)  # I


def _mid(p: Params) -> tuple[int, int]:
    """Bottom/top of a bar centred on mid-cap height."""
    lo = (p.cap - p.bar) // 2
    return lo, lo + p.bar


def _term(p: Params) -> int:
    """Terminal length of C/G/S/J beyond their horizontal bar."""
    return 2 * p.notch


def _tl(p: Params, c: Contour, i: int) -> list[Contour]:
    """Step the outer top-left vertex ``i`` (the face's signature)."""
    return [notch_corners(c, {i: p.notch})]


def _stair(p: Params, x0: float, y0: float, x1: float, y1: float, tv: float, th: float, n: int = 3) -> Contour:
    """Stair-step stroke climbing up-right from (x0, y0) to (x1, y1) in ``n`` steps.

    Horizontal treads are ``th`` thick, vertical risers ``tv`` wide. One polygon with
    4n+2 vertices at any weight. (Candidate for components.py: used by K X Y V Z.)
    """
    xs = [x0 + (x1 - tv - x0) * j // n for j in range(n + 1)]
    ys = [y0 + (y1 - th - y0) * j // n for j in range(n + 1)]
    pts = [(x0, y0)]
    for j in range(1, n + 1):
        pts += [(xs[j] + tv, ys[j - 1]), (xs[j] + tv, ys[j] + (th if j == n else 0))]
    for j in range(n, 0, -1):
        pts += [(xs[j], ys[j] + th), (xs[j], ys[j - 1] + th)]
    pts.append((x0, ys[0] + th))
    return polygon(*pts)


@glyph("A", 0x41, width=_cap)
def A(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo = (p.cap - b) // 3
    outer = polygon((x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap))
    return [notch_corners(outer, {6: p.notch, 7: p.notch}), rect(x0 + s, lo + b, x1 - s2, p.cap - b).counter()]


@glyph("B", 0x42, width=_cap)
def B(p: Params):
    x0, x1, s, s2, b, n = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, p.notch
    ym = p.cap // 2
    lo, hi = _mid(p)
    outer = polygon(
        (x0, 0), (x1, 0), (x1, ym - n), (x1 - n, ym - n), (x1 - n, ym + n), (x1, ym + n), (x1, p.cap), (x0, p.cap)
    )
    return [
        *_tl(p, outer, 7),
        rect(x0 + s, b, x1 - s2, lo).counter(),
        rect(x0 + s, hi, x1 - s2, p.cap - b).counter(),
    ]


@glyph("C", 0x43, width=_cap)
def C(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    c = polygon(
        (x0, 0), (x1, 0), (x1, b + t), (x1 - s2, b + t), (x1 - s2, b), (x0 + s, b), (x0 + s, p.cap - b),
        (x1 - s2, p.cap - b), (x1 - s2, p.cap - b - t), (x1, p.cap - b - t), (x1, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 11)


@glyph("D", 0x44, width=_cap)
def D(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl tr br")


@glyph("E", 0x45, width=_cap)
def E(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    lo, hi = _mid(p)
    xm = x1 - s
    c = polygon(
        (x0, 0), (x1, 0), (x1, b), (x0 + s, b), (x0 + s, lo), (xm, lo), (xm, hi), (x0 + s, hi),
        (x0 + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 11)


@glyph("F", 0x46, width=_cap)
def F(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    lo, hi = _mid(p)
    xm = x1 - s
    c = polygon(
        (x0, 0), (x0 + s, 0), (x0 + s, lo), (xm, lo), (xm, hi), (x0 + s, hi),
        (x0 + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 9)


@glyph("G", 0x47, width=_cap)
def G(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    yg = _mid(p)[1]
    xg = (x0 + x1) // 2
    c = polygon(
        (x0, 0), (x1, 0), (x1, yg), (xg, yg), (xg, yg - b), (x1 - s2, yg - b), (x1 - s2, b), (x0 + s, b),
        (x0 + s, p.cap - b), (x1 - s2, p.cap - b), (x1 - s2, p.cap - b - t), (x1, p.cap - b - t),
        (x1, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 13)


@glyph("H", 0x48, width=_cap)
def H(p: Params):
    x0, x1, s, s2 = p.sb, p.sb + p.cap_w, p.stem, p.stem2
    lo, hi = _mid(p)
    c = polygon(
        (x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0),
        (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, hi), (x0 + s, hi), (x0 + s, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 11)


@glyph("I", 0x49, width=_narrow)
def I(p: Params):
    return [notched_rect(p, p.sb, 0, p.sb + p.stem, p.cap, "tl")]


@glyph("J", 0x4A, width=_cap)
def J(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    c = polygon(
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s, p.cap), (x1 - s, b), (x0 + s2, b), (x0 + s2, b + t), (x0, b + t)
    )
    return _tl(p, c, 3)


@glyph("K", 0x4B, width=_cap)
def K(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    ym = p.cap // 2
    upper = _stair(p, x0 + s - s2, ym - b // 2, x1, p.cap, s2, b)
    return [notched_rect(p, x0, 0, x0 + s, p.cap, "tl"), upper, upper.flipped(ym)]


@glyph("L", 0x4C, width=_cap)
def L(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    return _tl(p, polygon((x0, 0), (x1, 0), (x1, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap)), 5)


@glyph("M", 0x4D, width=_wide)
def M(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + _wide_w(p), p.stem, p.stem2, p.bar
    m0 = (x0 + x1 - s2) // 2
    c = polygon(
        (x0, 0), (x0 + s, 0), (x0 + s, p.cap - b), (m0, p.cap - b), (m0, 0), (m0 + s2, 0), (m0 + s2, p.cap - b),
        (x1 - s2, p.cap - b), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 11)


@glyph("N", 0x4E, width=_cap)
def N(p: Params):
    return [arch(p, p.sb, p.sb + p.cap_w, p.cap, outer="tl", inner="tr")]


@glyph("O", 0x4F, width=_cap)
def O(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl", inner="tr")


@glyph("P", 0x50, width=_cap)
def P(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo, hi = _mid(p)
    outer = polygon((x0, 0), (x0 + s, 0), (x0 + s, lo), (x1, lo), (x1, p.cap), (x0, p.cap))
    return [*_tl(p, outer, 5), rect(x0 + s, hi, x1 - s2, p.cap - b).counter()]


@glyph("Q", 0x51, width=_cap)
def Q(p: Params):
    x1 = p.sb + p.cap_w
    tail = rect(x1 - 2 * p.stem2, -2 * p.notch, x1, p.bar)
    return [*frame(p, p.sb, 0, x1, p.cap, outer="tl", inner="tr"), tail]


@glyph("R", 0x52, width=_cap)
def R(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    lo, hi = _mid(p)
    outer = polygon((x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0), (x1, p.cap), (x0, p.cap))
    return [notch_corners(outer, {7: p.notch, 5: p.notch}), rect(x0 + s, hi, x1 - s2, p.cap - b).counter()]


@glyph("S", 0x53, width=_cap)
def S(p: Params):
    x0, x1, s, s2, b, t = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar, _term(p)
    lo, hi = _mid(p)
    c = polygon(
        (x0, 0), (x1, 0), (x1, hi), (x0 + s, hi), (x0 + s, p.cap - b), (x1 - s2, p.cap - b),
        (x1 - s2, p.cap - b - t), (x1, p.cap - b - t), (x1, p.cap), (x0, p.cap), (x0, lo),
        (x1 - s2, lo), (x1 - s2, b), (x0 + s, b), (x0 + s, b + t), (x0, b + t),
    )
    return _tl(p, c, 9)


@glyph("T", 0x54, width=_cap)
def T(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    cx = (x0 + x1 - s) // 2
    c = polygon(
        (cx, 0), (cx + s, 0), (cx + s, p.cap - b), (x1, p.cap - b), (x1, p.cap), (x0, p.cap), (x0, p.cap - b),
        (cx, p.cap - b),
    )
    return _tl(p, c, 5)


@glyph("U", 0x55, width=_cap)
def U(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + p.cap_w, p.stem, p.stem2, p.bar
    c = polygon(
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap)
    )
    return _tl(p, c, 7)


def _vee(p: Params, x0: float, x1: float, y0: float, y1: float, c: float) -> list[Contour]:
    """Two stair arms meeting at the centre line (heavy left arm, thin right arm)."""
    cx = (x0 + x1) // 2
    right = _stair(p, cx - c, y0, x1, y1, p.stem2, p.bar)
    return [right, _stair(p, cx - c, y0, x1, y1, p.stem, p.bar).mirrored(cx)]


@glyph("V", 0x56, width=_cap)
def V(p: Params):
    return _vee(p, p.sb, p.sb + p.cap_w, 0, p.cap, p.stem2)


@glyph("W", 0x57, width=_wide)
def W(p: Params):
    x0, x1, s, s2, b = p.sb, p.sb + _wide_w(p), p.stem, p.stem2, p.bar
    m0 = (x0 + x1 - s2) // 2
    top = p.cap - p.cap // 4
    c = polygon(
        (x0, 0), (x1, 0), (x1, p.cap), (x1 - s2, p.cap), (x1 - s2, b), (m0 + s2, b), (m0 + s2, top), (m0, top),
        (m0, b), (x0 + s, b), (x0 + s, p.cap), (x0, p.cap),
    )
    return _tl(p, c, 11)


@glyph("X", 0x58, width=_cap)
def X(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w
    cx = (x0 + x1) // 2
    return [
        _stair(p, x0, 0, x1, p.cap, p.stem2, p.bar),
        _stair(p, x0, 0, x1, p.cap, p.stem, p.bar).mirrored(cx),
    ]


@glyph("Y", 0x59, width=_cap)
def Y(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    ym = p.cap // 2
    stalk = rect((x0 + x1 - s) // 2, 0, (x0 + x1 + s) // 2, ym + b)
    return [*_vee(p, x0, x1, ym, p.cap, s // 2), stalk]


@glyph("Z", 0x5A, width=_cap)
def Z(p: Params):
    x0, x1, s, b = p.sb, p.sb + p.cap_w, p.stem, p.bar
    return [
        notched_rect(p, x0, p.cap - b, x1, p.cap, "tl"),
        rect(x0, 0, x1, b),
        _stair(p, x0, b // 2, x1, p.cap - b // 2, s, b),
    ]
