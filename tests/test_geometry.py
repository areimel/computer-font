from computerfont.geometry import Pt, Turtle, notch_corners, polygon, rect


def test_rect_is_ccw_with_positive_area():
    r = rect(0, 0, 10, 20)
    assert r.is_ccw and r.area == 200


def test_counter_is_clockwise():
    assert not rect(0, 0, 10, 20).counter().is_ccw


def test_turtle_builds_l_shape_ccw():
    c = Turtle(0, 0).h(100).v(40).h(-60).v(60).h(-40).close()
    assert len(c.pts) == 6 and c.is_ccw and c.area == 100 * 40 + 40 * 60


def test_turtle_cw_input_is_normalised_and_sharp_remapped():
    c = Turtle(0, 0).v(10).h(10, sharp=True).v(-10).close()
    assert c.is_ccw
    assert c.pts[next(iter(c.sharp))] == Pt(10, 10)


def test_turtle_drops_duplicate_closing_point():
    assert len(Turtle(0, 0).h(5).v(5).h(-5).v(-5).close().pts) == 4


def test_reverse_and_mirror_keep_sharp_points():
    c = Turtle(0, 0).h(10).v(10, sharp=True).h(-10).close()
    sharp_pt = c.pts[next(iter(c.sharp))]
    r = c.reversed()
    assert r.pts[next(iter(r.sharp))] == sharp_pt
    m = c.mirrored(0)
    assert m.is_ccw and Pt(-10, 10) in m.pts


def test_translate():
    assert rect(0, 0, 1, 1).translated(5, 7).pts[0] == Pt(5, 7)


def test_notch_corner_adds_step_and_removes_area():
    r = rect(0, 0, 100, 100)
    n = notch_corners(r, {3: 10})  # top-left
    assert len(n.pts) == 6 and n.is_ccw and n.area == 10000 - 100
    assert n.pts[4] in n.pts and 4 in n.sharp  # inner step vertex is sharp


def test_notch_on_concave_vertex_adds_material_to_counter():
    c = polygon((0, 0), (30, 0), (30, 50), (70, 50), (70, 0), (100, 0), (100, 100), (0, 100))
    n = notch_corners(c, {3: 10})
    assert n.area == c.area + 100
