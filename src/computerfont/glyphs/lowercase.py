"""Lowercase a-z (U+0061-007A). Rectilinear forms; diagonals are stepped blocks."""
from ..components import arch, dot, frame, notched_rect
from ..config import Params
from ..geometry import Contour, Pt, notch_corners
from ..registry import glyph


def _shape(p: Params, pts, tl=()) -> Contour:
    """One polygon from (x, y) points; vertices listed in ``tl`` get a square step."""
    c = notch_corners(Contour(tuple(Pt(*q) for q in pts)), {i: p.notch for i in tl})
    return c.oriented(True)


def _box(p: Params, w: int | None = None):
    return p.sb, p.sb + (p.lc_w if w is None else w)


def _lo(p: Params) -> int:
    """Bottom of a mid bar centred in the x-height."""
    return (p.xh - p.bar) // 2


def _bowl(p: Params, x0, x1) -> Contour:
    """Counter of a b/d/p/q bowl (hole with a notched top-right corner)."""
    return notched_rect(p, x0 + p.stem, p.bar, x1 - p.stem2, p.xh - p.bar, "tr").counter()


def _hook(p: Params, x0, x1, sw) -> Contour:
    """Descender hook (g j y): right stem, bottom bar, short tick up on the left."""
    d, b = p.desc, p.bar
    return _shape(p, [(x0, d), (x1, d), (x1, b // 2), (x1 - sw, b // 2), (x1 - sw, d + b),
                      (x0 + p.stem2, d + b), (x0 + p.stem2, d + b + p.notch), (x0, d + b + p.notch)])


def _w_narrow(p: Params) -> int:
    return p.stem + 2 * p.notch


def _dot_over(p: Params, cx) -> Contour:
    return dot(p, cx, p.xh + p.bar // 2 + p.dot / 2)


@glyph("a", 0x61, width=lambda p: p.adv(p.lc_w))
def a(p: Params):
    x0, x1 = _box(p)
    s, s2, b, lo, xh = p.stem, p.stem2, p.bar, _lo(p), p.xh
    out = _shape(p, [(x0, 0), (x1, 0), (x1, xh), (x0, xh), (x0, xh - b), (x1 - s2, xh - b),
                     (x1 - s2, lo + b), (x0, lo + b)], tl=(3,))
    return [out, notched_rect(p, x0 + s, b, x1 - s2, lo, "tr").counter()]


@glyph("b", 0x62, width=lambda p: p.adv(p.lc_w))
def b(p: Params):
    x0, x1 = _box(p)
    return [_shape(p, [(x0, 0), (x1, 0), (x1, p.xh), (x0 + p.stem, p.xh), (x0 + p.stem, p.asc),
                       (x0, p.asc)], tl=(5,)), _bowl(p, x0, x1)]


@glyph("c", 0x63, width=lambda p: p.adv(p.lc_w))
def c(p: Params):
    x0, x1 = _box(p)
    s, bb, xh = p.stem, p.bar, p.xh
    return [_shape(p, [(x0, 0), (x1, 0), (x1, bb), (x0 + s, bb), (x0 + s, xh - bb), (x1, xh - bb),
                       (x1, xh), (x0, xh)], tl=(7,))]


@glyph("d", 0x64, width=lambda p: p.adv(p.lc_w))
def d(p: Params):
    x0, x1 = _box(p)
    return [_shape(p, [(x0, 0), (x1, 0), (x1, p.asc), (x1 - p.stem2, p.asc), (x1 - p.stem2, p.xh),
                       (x0, p.xh)], tl=(5,)), _bowl(p, x0, x1)]


@glyph("e", 0x65, width=lambda p: p.adv(p.lc_w))
def e(p: Params):
    x0, x1 = _box(p)
    s, s2, bb, lo, xh = p.stem, p.stem2, p.bar, _lo(p), p.xh
    out = _shape(p, [(x0, 0), (x1, 0), (x1, bb), (x0 + s, bb), (x0 + s, lo), (x1, lo), (x1, xh),
                     (x0, xh)], tl=(7,))
    return [out, notched_rect(p, x0 + s, lo + bb, x1 - s2, xh - bb, "tr").counter()]


@glyph("f", 0x66, width=lambda p: p.adv(p.lc_w * 3 // 4))
def f(p: Params):
    x0, x1 = _box(p, p.lc_w * 3 // 4)
    xl = x0 + 2 * p.notch
    xr, bb, xh, asc = xl + p.stem, p.bar, p.xh, p.asc
    return [_shape(p, [(xl, 0), (xr, 0), (xr, xh - bb), (x1, xh - bb), (x1, xh), (xr, xh), (xr, asc - bb),
                       (x1, asc - bb), (x1, asc), (xl, asc), (xl, xh), (x0, xh), (x0, xh - bb),
                       (xl, xh - bb)], tl=(9,))]


@glyph("g", 0x67, width=lambda p: p.adv(p.lc_w))
def g(p: Params):
    x0, x1 = _box(p)
    return [*frame(p, x0, 0, x1, p.xh, outer="tl", inner="tr"), _hook(p, x0, x1, p.stem2)]


@glyph("h", 0x68, width=lambda p: p.adv(p.lc_w))
def h(p: Params):
    x0, x1 = _box(p)
    s, s2, bb, xh = p.stem, p.stem2, p.bar, p.xh
    out = _shape(p, [(x0, 0), (x0 + s, 0), (x0 + s, xh - bb), (x1 - s2, xh - bb), (x1 - s2, 0), (x1, 0),
                     (x1, xh), (x0 + s, xh), (x0 + s, p.asc), (x0, p.asc)], tl=(9, 3))
    return [out]


@glyph("i", 0x69, width=lambda p: p.adv(_w_narrow(p)))
def i(p: Params):
    x0, x1 = _box(p, _w_narrow(p))
    return [_shape(p, [(x0 + p.notch, 0), (x1 - p.notch, 0), (x1 - p.notch, p.xh), (x0 + p.notch, p.xh)], tl=(3,)),
            _dot_over(p, (x0 + x1) / 2)]


@glyph("j", 0x6A, width=lambda p: p.adv(p.lc_w * 5 // 8))
def j(p: Params):
    x0, x1 = _box(p, p.lc_w * 5 // 8)
    return [_shape(p, [(x1 - p.stem, p.bar, ), (x1, p.bar), (x1, p.xh), (x1 - p.stem, p.xh)], tl=(3,)),
            _hook(p, x0, x1, p.stem), _dot_over(p, x1 - p.stem / 2)]


@glyph("k", 0x6B, width=lambda p: p.adv(p.lc_w))
def k(p: Params):
    x0, x1 = _box(p)
    s, s2, bb, n, lo, xh = p.stem, p.stem2, p.bar, p.notch, _lo(p), p.xh
    return [_shape(p, [(x0, 0), (x0 + s, 0), (x0 + s, lo), (x1 - s2, lo), (x1 - s2, 0), (x1, 0),
                       (x1, lo + bb), (x1 - n, lo + bb), (x1 - n, xh), (x1 - s2 - n, xh),
                       (x1 - s2 - n, lo + bb), (x0 + s, lo + bb), (x0 + s, p.asc), (x0, p.asc)], tl=(13,))]


@glyph("l", 0x6C, width=lambda p: p.adv(_w_narrow(p)))
def l(p: Params):
    x0, x1 = _box(p, _w_narrow(p))
    return [_shape(p, [(x0 + p.notch, 0), (x1 - p.notch, 0), (x1 - p.notch, p.asc), (x0 + p.notch, p.asc)], tl=(3,))]


@glyph("m", 0x6D, width=lambda p: p.adv(p.lc_w * 3 // 2))
def m(p: Params):
    x0, x1 = _box(p, p.lc_w * 3 // 2)
    s, s2, bb, xh = p.stem, p.stem2, p.bar, p.xh
    m0 = x0 + s + (x1 - x0 - s - 2 * s2) // 2
    return [_shape(p, [(x0, 0), (x0 + s, 0), (x0 + s, xh - bb), (m0, xh - bb), (m0, 0), (m0 + s2, 0),
                       (m0 + s2, xh - bb), (x1 - s2, xh - bb), (x1 - s2, 0), (x1, 0), (x1, xh),
                       (x0, xh)], tl=(11, 3, 7))]


@glyph("n", 0x6E, width=lambda p: p.adv(p.lc_w))
def n(p: Params):
    return [arch(p, p.sb, p.sb + p.lc_w, p.xh, outer="tl", inner="tr")]


@glyph("o", 0x6F, width=lambda p: p.adv(p.lc_w))
def o(p: Params):
    return frame(p, p.sb, 0, p.sb + p.lc_w, p.xh, outer="tl", inner="tr")


@glyph("p", 0x70, width=lambda p: p.adv(p.lc_w))
def p_(p: Params):
    x0, x1 = _box(p)
    return [_shape(p, [(x0, p.desc), (x0 + p.stem, p.desc), (x0 + p.stem, 0), (x1, 0), (x1, p.xh),
                       (x0, p.xh)], tl=(5,)), _bowl(p, x0, x1)]


@glyph("q", 0x71, width=lambda p: p.adv(p.lc_w))
def q(p: Params):
    x0, x1 = _box(p)
    return [_shape(p, [(x1 - p.stem2, p.desc), (x1, p.desc), (x1, p.xh), (x0, p.xh), (x0, 0),
                       (x1 - p.stem2, 0)], tl=(3,)), _bowl(p, x0, x1)]


@glyph("r", 0x72, width=lambda p: p.adv(p.lc_w * 3 // 4))
def r(p: Params):
    x0, x1 = _box(p, p.lc_w * 3 // 4)
    s, s2, bb, xh = p.stem, p.stem2, p.bar, p.xh
    return [_shape(p, [(x0, 0), (x0 + s, 0), (x0 + s, xh - bb), (x1 - s2, xh - bb), (x1 - s2, xh - 2 * bb),
                       (x1, xh - 2 * bb), (x1, xh), (x0, xh)], tl=(7,))]


@glyph("s", 0x73, width=lambda p: p.adv(p.lc_w))
def s(p: Params):
    x0, x1 = _box(p)
    st, s2, bb, lo, xh = p.stem, p.stem2, p.bar, _lo(p), p.xh
    return [_shape(p, [(x0, 0), (x1, 0), (x1, lo + bb), (x0 + st, lo + bb), (x0 + st, xh - bb), (x1, xh - bb),
                       (x1, xh), (x0, xh), (x0, lo), (x1 - s2, lo), (x1 - s2, bb), (x0, bb)], tl=(7,))]


@glyph("t", 0x74, width=lambda p: p.adv(p.lc_w * 3 // 4))
def t(p: Params):
    x0, x1 = _box(p, p.lc_w * 3 // 4)
    xl = x0 + 2 * p.notch
    xr, bb, xh = xl + p.stem, p.bar, p.xh
    top = xh + (p.asc - xh) // 2
    return [_shape(p, [(xl, 0), (x1, 0), (x1, bb), (xr, bb), (xr, xh - bb), (x1, xh - bb), (x1, xh),
                       (xr, xh), (xr, top), (xl, top), (xl, xh), (x0, xh), (x0, xh - bb),
                       (xl, xh - bb)], tl=(9,))]


@glyph("u", 0x75, width=lambda p: p.adv(p.lc_w))
def u(p: Params):
    x0, x1 = _box(p)
    return [_shape(p, [(x0, 0), (x1, 0), (x1, p.xh), (x1 - p.stem2, p.xh), (x1 - p.stem2, p.bar),
                       (x0 + p.stem, p.bar), (x0 + p.stem, p.xh), (x0, p.xh)], tl=(7,))]


@glyph("v", 0x76, width=lambda p: p.adv(p.lc_w))
def v(p: Params):
    """Stepped V: three tiers, each band shifted inward by dd; bottom tier merges."""
    x0, x1 = _box(p)
    s, s2, xh = p.stem, p.stem2, p.xh
    dd = (p.lc_w - s - s2) // 4
    tl_, tr_ = s + dd * 3 // 4, s2 + dd * 3 // 4
    h1, h2 = xh // 3, 2 * (xh // 3)
    return [_shape(p, [(x0 + 2 * dd, 0), (x1 - 2 * dd, 0), (x1 - 2 * dd, h1), (x1 - dd, h1), (x1 - dd, h2),
                       (x1, h2), (x1, xh), (x1 - tr_, xh), (x1 - tr_, h2), (x1 - dd - tr_, h2),
                       (x1 - dd - tr_, h1), (x0 + dd + tl_, h1), (x0 + dd + tl_, h2), (x0 + tl_, h2),
                       (x0 + tl_, xh), (x0, xh), (x0, h2), (x0 + dd, h2), (x0 + dd, h1),
                       (x0 + 2 * dd, h1)], tl=(15,))]


@glyph("w", 0x77, width=lambda p: p.adv(p.lc_w * 3 // 2))
def w(p: Params):
    x0, x1 = _box(p, p.lc_w * 3 // 2)
    s, s2, bb, xh = p.stem, p.stem2, p.bar, p.xh
    m0 = x0 + s + (x1 - x0 - s - 2 * s2) // 2
    ym = xh - 2 * bb
    return [_shape(p, [(x0, 0), (x1, 0), (x1, xh), (x1 - s2, xh), (x1 - s2, bb), (m0 + s2, bb), (m0 + s2, ym),
                       (m0, ym), (m0, bb), (x0 + s, bb), (x0 + s, xh), (x0, xh)], tl=(11,))]


@glyph("x", 0x78, width=lambda p: p.adv(p.lc_w))
def x(p: Params):
    """Waisted X: two legs top and bottom meeting in a narrower central block."""
    x0, x1 = _box(p)
    s, s2, xh, e = p.stem, p.stem2, p.xh, p.notch
    h1 = _lo(p)
    h2 = h1 + p.bar
    return [_shape(p, [(x0, 0), (x0 + s, 0), (x0 + s, h1), (x1 - s2, h1), (x1 - s2, 0), (x1, 0), (x1, h1),
                       (x1 - e, h1), (x1 - e, h2), (x1, h2), (x1, xh), (x1 - s2, xh), (x1 - s2, h2),
                       (x0 + s, h2), (x0 + s, xh), (x0, xh), (x0, h2), (x0 + e, h2), (x0 + e, h1),
                       (x0, h1)], tl=(15,))]


@glyph("y", 0x79, width=lambda p: p.adv(p.lc_w))
def y(p: Params):
    x0, x1 = _box(p)
    return [u(p)[0], _hook(p, x0, x1, p.stem2)]


@glyph("z", 0x7A, width=lambda p: p.adv(p.lc_w))
def z(p: Params):
    """Stepped Z (mirror of s): top bar, right riser, mid bar, left riser, bottom bar."""
    x0, x1 = _box(p)
    s, s2, bb, lo, xh = p.stem, p.stem2, p.bar, _lo(p), p.xh
    return [_shape(p, [(x0, 0), (x1, 0), (x1, bb), (x0 + s, bb), (x0 + s, lo), (x1, lo), (x1, xh),
                       (x0, xh), (x0, xh - bb), (x1 - s2, xh - bb), (x1 - s2, lo + bb), (x0, lo + bb)], tl=(7,))]
