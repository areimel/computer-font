from computerfont import config as C
from computerfont.kerning import KERN1, KERN2, LEFT, PAIRS, RIGHT, groups, kerning
from computerfont.registry import all_glyphs
from computerfont.spacing import BEARINGS, space_width

NAMES = {g.name for g in all_glyphs()}


def test_groups_reference_existing_glyphs():
    for key, members in groups().items():
        assert set(members) <= NAMES, key


def test_glyph_in_one_group_per_side():
    for table in (LEFT, RIGHT):
        seen = [n for v in table.values() for n in v.split()]
        assert len(seen) == len(set(seen))


def test_pairs_reference_defined_groups():
    for a, b, v in PAIRS:
        assert a in LEFT and b in RIGHT and v < 0


def test_kerning_scales_with_master():
    light, black = (kerning(C.Params.at(w)) for w in (200, 900))
    assert light.keys() == black.keys()
    assert all(black[k] <= light[k] < 0 for k in light)
    assert all(k[0].startswith(KERN1) and k[1].startswith(KERN2) for k in light)


def test_spacing_table_and_space_width():
    assert set(BEARINGS) <= NAMES
    for w in (200, 900):
        assert 250 <= space_width(C.Params.at(w)) <= 300
