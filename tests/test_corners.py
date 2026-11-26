import pytest

from computerfont.corners import corner_points, draw_contour, round_contour
from computerfont.geometry import Pt, polygon, rect
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.pens.recordingPen import RecordingPointPen


def test_r0_gives_four_coincident_points_per_vertex():
    c = polygon((0, 0), (30, 0), (30, 50), (70, 50), (70, 0), (100, 0), (100, 100), (0, 100))
    for quad, p in zip(round_contour(c, 0), c.pts):
        assert set(quad) == {p}


def _point_count(c, r, ndigits=0):
    rec = RecordingPointPen()
    draw_contour(SegmentToPointPen(rec), c, r, ndigits=ndigits)
    return sum(op == "addPoint" for op, _, _ in rec.value)


def test_point_count_is_four_per_vertex():
    c = rect(0, 0, 100, 100)
    assert _point_count(c, 20, ndigits=None) == 4 * len(c.pts)
    assert _point_count(c, 0) == 4 * len(c.pts)
    assert _point_count(c, 50) == 4 * len(c.pts)  # edges fully consumed by rounding


def test_corner_geometry():
    a, c1, c2, b = corner_points(Pt(0, 0), Pt(100, 0), Pt(100, 100), 20)
    assert a == Pt(80, 0) and b == Pt(100, 20)
    assert c1.y == 0 and c1.x == pytest.approx(80 + 0.5523 * 20, abs=0.01)
    assert c2.x == 100 and c2.y == pytest.approx(20 - 0.5523 * 20, abs=0.01)


def test_radius_clamped_to_half_of_shortest_edge():
    a, _, _, b = corner_points(Pt(0, 0), Pt(100, 0), Pt(100, 30), 50)
    assert a == Pt(85, 0) and b == Pt(100, 15)  # edge of 30 -> r = 15


def test_sharp_vertices_never_round():
    c = polygon((0, 0), (100, 0), (100, 100), (0, 100))
    from computerfont.geometry import Contour

    c = Contour(c.pts, frozenset({2}))
    quads = round_contour(c, 20)
    assert set(quads[2]) == {c.pts[2]} and len(set(quads[1])) > 1
