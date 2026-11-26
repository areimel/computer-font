"""Reusable shape builders. Glyph files compose these; all take a ``Params``.

Coordinates are absolute font units, baseline y=0. Builders return ``Contour``
(or a list of them); outers are CCW, counters CW. Strokes that meet should
*overlap* (never just touch); overlaps are kept in the final font.
"""
from __future__ import annotations

from .config import Params
from .geometry import Contour, notch_corners, polygon, rect

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

