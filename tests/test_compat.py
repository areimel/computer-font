"""Every glyph must have identical point structure in all masters."""
import pytest
from fontTools.pens.recordingPen import RecordingPen

from computerfont import config as C
from computerfont.corners import draw_contour
from computerfont.registry import all_glyphs


def _structure(g, wght, rond):
    p = C.Params.at(wght, rond)
    out = []
    for c in g.contours(p):
        pen = RecordingPen()
        draw_contour(pen, c, p.radius)
        out.append([(op, len(args)) for op, args in pen.value])
    return out


@pytest.mark.parametrize("g", all_glyphs(), ids=lambda g: g.name)
def test_structure_identical_across_masters(g):
    ref = _structure(g, *C.DEFAULT_MASTER)
    for loc in C.ALL_MASTERS:
        assert _structure(g, *loc) == ref, f"{g.name} differs at {loc}"


@pytest.mark.parametrize("g", all_glyphs(), ids=lambda g: g.name)
def test_winding_outer_ccw_counter_cw(g):
    for loc in C.ALL_MASTERS:
        cs = g.contours(C.Params.at(*loc))
        assert all(c.area != 0 for c in cs)
        # The largest contour is the outer one for every glyph with a counter.
        if len(cs) > 1:
            assert max(cs, key=lambda c: abs(c.area)).is_ccw


def test_master_params_are_linear_in_wght():
    lo, mid, hi = (C.Params.at(w, 0) for w in (200, 400, 900))
    assert abs(mid.stem - (lo.stem + (hi.stem - lo.stem) * 200 / 700)) <= 1
