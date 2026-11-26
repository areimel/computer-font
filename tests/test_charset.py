import pytest

from computerfont.registry import all_glyphs

ASCII = set(range(0x20, 0x7F))


def test_registered_unicodes_are_printable_ascii():
    for g in all_glyphs():
        assert g.unicode is None or g.unicode in ASCII, g.name


def test_no_duplicate_unicodes_and_required_glyphs():
    uni = [g.unicode for g in all_glyphs() if g.unicode is not None]
    assert len(uni) == len(set(uni))
    names = [g.name for g in all_glyphs()]
    assert names[0] == ".notdef" and "space" in names


@pytest.mark.xfail(strict=False, reason="remaining glyphs not drawn yet")
def test_full_ascii_coverage():
    have = {g.unicode for g in all_glyphs()}
    assert ASCII <= have
