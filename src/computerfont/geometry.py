"""Points, closed contours, an orthogonal 'turtle' builder, and notch/transform helpers."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, NamedTuple


class Pt(NamedTuple):
    x: float
    y: float


def _signed_area(pts: list[Pt]) -> float:
    return 0.5 * sum(a.x * b.y - b.x * a.y for a, b in zip(pts, pts[1:] + pts[:1]))


def _unit(a: Pt, b: Pt) -> Pt:
    dx, dy = b.x - a.x, b.y - a.y
    n = (dx * dx + dy * dy) ** 0.5
    return Pt(dx / n, dy / n) if n else Pt(0, 0)


@dataclass(frozen=True)
class Contour:
    """Closed polygon. UFO convention: outer shapes counter-clockwise (area > 0),
    counters clockwise (area < 0). ``sharp`` holds vertex indices never rounded."""

    pts: tuple[Pt, ...]
    sharp: frozenset[int] = field(default_factory=frozenset)

    @property
    def area(self) -> float:
        return _signed_area(list(self.pts))

    @property
    def is_ccw(self) -> bool:
        return self.area > 0

    def reversed(self) -> "Contour":
        n = len(self.pts)
        return Contour(self.pts[::-1], frozenset(n - 1 - i for i in self.sharp))

    def oriented(self, ccw: bool) -> "Contour":
        return self if self.is_ccw == ccw else self.reversed()

    def counter(self) -> "Contour":
        """This shape as a hole (clockwise)."""
        return self.oriented(False)

    def translated(self, dx: float, dy: float = 0) -> "Contour":
        return Contour(tuple(Pt(p.x + dx, p.y + dy) for p in self.pts), self.sharp)

    def mirrored(self, axis_x: float) -> "Contour":
        """Mirror about vertical line x=axis_x (orientation is re-normalised)."""
        m = Contour(tuple(Pt(2 * axis_x - p.x, p.y) for p in self.pts), self.sharp)
        return m.reversed()

    def flipped(self, axis_y: float) -> "Contour":
        """Mirror about horizontal line y=axis_y (orientation is re-normalised)."""
        m = Contour(tuple(Pt(p.x, 2 * axis_y - p.y) for p in self.pts), self.sharp)
        return m.reversed()


def rect(x0: float, y0: float, x1: float, y1: float, sharp: Iterable[int] = ()) -> Contour:
    """Counter-clockwise rectangle starting bottom-left."""
    x0, x1 = sorted((x0, x1))
    y0, y1 = sorted((y0, y1))
    return Contour((Pt(x0, y0), Pt(x1, y0), Pt(x1, y1), Pt(x0, y1)), frozenset(sharp))


def polygon(*pts: tuple[float, float], ccw: bool = True) -> Contour:
    """Contour from (x, y) tuples, normalised to the requested orientation."""
    return Contour(tuple(Pt(*p) for p in pts)).oriented(ccw)


class Turtle:
    """Relative orthogonal builder: ``Turtle(0,0).h(100).v(50).h(-100).close()``.

    ``sharp=True`` on a move marks the vertex it arrives at as never-rounded.
    ``close()`` returns an outer (CCW) contour, or a counter (CW) if ``counter=True``.
    """

    def __init__(self, x: float, y: float, sharp: bool = False):
        self._pts = [Pt(x, y)]
        self._sharp = {0} if sharp else set()

    def to(self, x: float, y: float, sharp: bool = False) -> "Turtle":
        if sharp:
            self._sharp.add(len(self._pts))
        self._pts.append(Pt(x, y))
        return self

    def h(self, dx: float, sharp: bool = False) -> "Turtle":
        last = self._pts[-1]
        return self.to(last.x + dx, last.y, sharp)

    def v(self, dy: float, sharp: bool = False) -> "Turtle":
        last = self._pts[-1]
        return self.to(last.x, last.y + dy, sharp)

    def close(self, counter: bool = False) -> Contour:
        pts = list(self._pts)
        if len(pts) > 1 and pts[-1] == pts[0]:
            pts.pop()
            self._sharp.discard(len(pts))
        c = Contour(tuple(pts), frozenset(self._sharp))
        return c.oriented(not counter)


def notch_corners(c: Contour, cuts: dict[int, float]) -> Contour:
    """Replace each vertex ``i`` in ``cuts`` with a square step of size ``cuts[i]``.

    The vertex becomes three: a point back along the incoming edge, a (sharp) inner
    point, and a point along the outgoing edge. Works for convex and concave
    vertices (concave ones add a step of material into the counter).
    """
    n = len(c.pts)
    out: list[Pt] = []
    sharp: set[int] = set()
    for i, p in enumerate(c.pts):
        size = cuts.get(i)
        if not size:
            if i in c.sharp:
                sharp.add(len(out))
            out.append(p)
            continue
        d_in = _unit(c.pts[i - 1], p)
        d_out = _unit(p, c.pts[(i + 1) % n])
        a = Pt(p.x - d_in.x * size, p.y - d_in.y * size)
        b = Pt(a.x + d_out.x * size, a.y + d_out.y * size)
        e = Pt(p.x + d_out.x * size, p.y + d_out.y * size)
        out.append(a)
        sharp.add(len(out))
        out.append(b)
        out.append(e)
    return Contour(tuple(out), frozenset(sharp))
