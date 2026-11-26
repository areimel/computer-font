"""Interpolation-safe corner rounding: every vertex becomes one cubic (4 points)."""
from __future__ import annotations

from typing import Protocol

from .geometry import Contour, Pt

KAPPA = 0.5522847498


class SegmentPen(Protocol):
    def moveTo(self, pt): ...
    def lineTo(self, pt): ...
    def curveTo(self, *pts): ...
    def closePath(self): ...


def corner_points(prev: Pt, p: Pt, nxt: Pt, r: float) -> tuple[Pt, Pt, Pt, Pt]:
    """(on, off, off, on) for the corner at ``p``; r is clamped to half of each edge.

    With r == 0 all four points equal ``p``.
    """
    lin = ((p.x - prev.x) ** 2 + (p.y - prev.y) ** 2) ** 0.5
    lout = ((nxt.x - p.x) ** 2 + (nxt.y - p.y) ** 2) ** 0.5
    r = max(0.0, min(r, lin / 2, lout / 2))
    if r == 0:
        return p, p, p, p
    din = Pt((p.x - prev.x) / lin, (p.y - prev.y) / lin)
    dout = Pt((nxt.x - p.x) / lout, (nxt.y - p.y) / lout)
    a = Pt(p.x - din.x * r, p.y - din.y * r)
    b = Pt(p.x + dout.x * r, p.y + dout.y * r)
    k = KAPPA * r
    return a, Pt(a.x + din.x * k, a.y + din.y * k), Pt(b.x - dout.x * k, b.y - dout.y * k), b


def round_contour(c: Contour, r: float) -> list[tuple[Pt, Pt, Pt, Pt]]:
    """Per-vertex corner quads for a contour; ``sharp`` vertices always use r=0."""
    n = len(c.pts)
    return [
        corner_points(c.pts[i - 1], c.pts[i], c.pts[(i + 1) % n], 0 if i in c.sharp else r)
        for i in range(n)
    ]


def draw_contour(pen: SegmentPen, c: Contour, r: float, ndigits: int | None = 0) -> None:
    """Draw ``c`` into a segment pen as a closed path of 4*len(pts) points."""

    def q(pt: Pt):
        if ndigits is None:
            return (pt.x, pt.y)
        return (round(pt.x), round(pt.y)) if ndigits == 0 else (round(pt.x, ndigits), round(pt.y, ndigits))

    # Start at the end of corner 0 and finish with corner 0's curve, so the path
    # always closes on a curve that lands exactly on the start point. Closing on a
    # line instead lets point pens drop it when it has zero length (r clamped to
    # half the edge), which changes the point count in some masters only.
    quads = round_contour(c, r)
    pen.moveTo(q(quads[0][3]))
    for a, c1, c2, b in quads[1:] + quads[:1]:
        pen.lineTo(q(a))
        pen.curveTo(q(c1), q(c2), q(b))
    pen.closePath()
