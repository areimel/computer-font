"""Reusable shape builders. Glyph files compose these; all take a ``Params``.

Coordinates are absolute font units, baseline y=0. Builders return ``Contour``
(or a list of them); outers are CCW, counters CW. Strokes that meet should
*overlap* (never just touch); overlaps are kept in the final font.
"""
from __future__ import annotations

from .config import Params
from .geometry import Contour, Pt, notch_corners, polygon, rect

# Corner indices of a rectangle contour (CCW from bottom-left).
BL, BR, TR, TL = 0, 1, 2, 3
_CORNER = {"bl": BL, "br": BR, "tr": TR, "tl": TL}


def stem(p: Params, x: float, y0: float, y1: float, w: float | None = None) -> Contour:
    """Vertical stroke with left edge at ``x`` spanning y0..y1 (default width p.stem)."""
    return rect(x, y0, x + (p.stem if w is None else w), y1)


def bar(p: Params, x0: float, x1: float, y: float, t: float | None = None, align: str = "bottom") -> Contour:
    """Horizontal stroke x0..x1. ``y`` is its bottom/top/center per ``align``."""
    t = p.bar if t is None else t
    lo = {"bottom": y, "top": y - t, "center": y - t / 2}[align]
    return rect(x0, lo, x1, lo + t)


def notched_rect(
    p: Params, x0: float, y0: float, x1: float, y1: float, corners: str = "", n: float | None = None
) -> Contour:
    """Rectangle with square steps cut into the named corners, e.g. ``"tl"`` or ``"tl br"``.

    Vertex count is 4 + 2*len(corners) regardless of weight, so it is master-safe.
    """
    n = p.notch if n is None else n
    cuts = {_CORNER[c]: n for c in corners.split()}
    return notch_corners(rect(x0, y0, x1, y1), cuts)


def frame(
    p: Params,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    outer: str = "",
    inner: str = "",
    sides: float | None = None,
    bars: float | None = None,
) -> list[Contour]:
    """Rectangular ring: outer shape + square counter, each with optional notched corners.

    Left side uses ``p.stem``, right side ``p.stem2`` (the style's contrast);
    ``sides``/``bars`` override the vertical/horizontal stroke thickness.
    """
    sl, sr = (p.stem, p.stem2) if sides is None else (sides, sides)
    b = p.bar if bars is None else bars
    return [
        notched_rect(p, x0, y0, x1, y1, outer),
        notched_rect(p, x0 + sl, y0 + b, x1 - sr, y1 - b, inner).counter(),
    ]


def dot(p: Params, cx: float, cy: float, size: float | None = None) -> Contour:
    """Square dot centred on (cx, cy)."""
    d = p.dot if size is None else size
    return rect(cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2)


def arch(p: Params, x0: float, x1: float, y1: float, outer: str = "tl", inner: str = "tr") -> Contour:
    """Inverted-U (n-shape) from the baseline up to y1: two stems joined by a top bar.

    ``outer``/``inner`` name corners to notch ("tl"/"tr" outer; "tl"/"tr" of the counter).
    """
    s, s2, b = p.stem, p.stem2, p.bar
    pts = [(x0, 0), (x0 + s, 0), (x0 + s, y1 - b), (x1 - s2, y1 - b), (x1 - s2, 0), (x1, 0), (x1, y1), (x0, y1)]
    # indices: 7 = outer TL, 6 = outer TR, 2 = counter TL, 3 = counter TR
    idx = {"tl": 7, "tr": 6}
    inn = {"tl": 2, "tr": 3}
    cuts = {idx[c]: p.notch for c in outer.split()}
    cuts.update({inn[c]: p.notch for c in inner.split()})
    return notch_corners(polygon(*pts), cuts)



# ---- widths ---------------------------------------------------------------

def cap_width(p: Params) -> int:
    """Advance width of a standard capital box (``p.cap_w``)."""
    return p.adv(p.cap_w)


def lc_width(p: Params) -> int:
    """Advance width of a standard lowercase / digit box (``p.lc_w``)."""
    return p.adv(p.lc_w)


# ---- vertical positions ---------------------------------------------------

def mid_bar(p: Params, height: float | None = None) -> tuple[int, int]:
    """(bottom, top) of a ``p.bar``-thick bar centred in ``height`` (default cap height)."""
    lo = ((p.cap if height is None else height) - p.bar) // 2
    return lo, lo + p.bar


def math_axis(p: Params) -> int:
    """Vertical middle of the x-height, where operators (+ < = > ~) are centred."""
    return p.xh // 2


# ---- polygons -------------------------------------------------------------

def notched_poly(p: Params, pts, tl: int | tuple[int, ...] = (), flip: float | None = None) -> Contour:
    """Orthogonal polygon (CCW) with the face's square step cut at vertex index/indices ``tl``.

    ``flip`` mirrors x about flip/2 (pass x0 + x1) so a right-hand variant of a
    left-hand outline keeps its point order; ``tl`` then names the mirrored vertex.
    """
    if isinstance(tl, int):
        tl = (tl,)
    if flip is not None:
        pts = [(flip - x, y) for x, y in pts]
    c = notch_corners(Contour(tuple(Pt(*q) for q in pts)), {i: p.notch for i in tl})
    return c.oriented(True)


def stair(x0: float, y0: float, x1: float, y1: float, tv: float, th: float, n: int = 3) -> Contour:
    """Stair-step stroke climbing up-right from (x0, y0) to (x1, y1) in ``n`` steps.

    Horizontal treads are ``th`` thick, vertical risers ``tv`` wide. One polygon with
    4n+2 vertices at any weight (the face's orthogonal "diagonal": K X Y V Z).
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


def s_shape(p: Params, x0: float, y0: float, x1: float, y1: float, tl: bool = False) -> Contour:
    """Blocky S in one 12-point polygon (5, s, $): top bar, left upper stem, middle
    bar, right lower stem, bottom bar. ``tl`` steps the top-left corner."""
    s, s2, b = p.stem, p.stem2, p.bar
    lo, hi = mid_bar(p, y0 + y1)
    pts = [(x0, y0), (x1, y0), (x1, hi), (x0 + s, hi), (x0 + s, y1 - b), (x1, y1 - b),
           (x1, y1), (x0, y1), (x0, lo), (x1 - s2, lo), (x1 - s2, y0 + b), (x0, y0 + b)]
    return notched_poly(p, pts, tl=7 if tl else ())


def tail_dot(p: Params, x: float, y: float, h: float | None = None) -> Contour:
    """Square dot with lower-left corner (x, y) and a half-width tail hanging ``h`` below it."""
    d, h = p.dot, p.dot if h is None else h
    return notched_poly(p, [(x + d / 2, y - h), (x + d, y - h), (x + d, y + d), (x, y + d), (x, y), (x + d / 2, y)])


def desc_hook(p: Params, x0: float, x1: float, sw: float) -> Contour:
    """Descender hook (g j y): right stem ``sw`` wide, bottom bar, short tick up on the left."""
    d, b = p.desc, p.bar
    return notched_poly(p, [(x0, d), (x1, d), (x1, b // 2), (x1 - sw, b // 2), (x1 - sw, d + b),
                            (x0 + p.stem2, d + b), (x0 + p.stem2, d + b + p.notch), (x0, d + b + p.notch)])


def bowl_counter(p: Params, x0: float, x1: float) -> Contour:
    """Counter of a b/d/p/q bowl (hole with a notched top-right corner)."""
    return notched_rect(p, x0 + p.stem, p.bar, x1 - p.stem2, p.xh - p.bar, "tr").counter()
