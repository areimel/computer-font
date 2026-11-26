"""Build a ufoLib2 Font for one (wght, rond) master location."""
from __future__ import annotations

from pathlib import Path

import ufoLib2

from . import config as C
from .corners import draw_contour
from .registry import all_glyphs


def master_filename(wght: int, rond: int) -> str:
    return f"{C.FILE_STEM}-{C.style_name(wght, rond).replace(' ', '')}.ufo"


def build_ufo(wght: int, rond: int) -> ufoLib2.Font:
    p = C.Params.at(wght, rond)
    style = C.style_name(wght, rond)
    font = ufoLib2.Font()
    i = font.info
    i.familyName = C.FAMILY_NAME
    i.styleName = style
    i.unitsPerEm = C.UPM
    i.ascender, i.descender = C.ASCENDER, C.DESCENDER
    i.capHeight, i.xHeight = C.CAP_HEIGHT, C.X_HEIGHT
    i.versionMajor, i.versionMinor = C.VERSION
    i.openTypeOS2WeightClass = wght
    i.openTypeOS2TypoAscender, i.openTypeOS2TypoDescender, i.openTypeOS2TypoLineGap = C.ASCENDER, C.DESCENDER, 0
    i.openTypeOS2WinAscent, i.openTypeOS2WinDescent = C.ASCENDER + 40, -C.DESCENDER + 40
    i.openTypeHheaAscender, i.openTypeHheaDescender, i.openTypeHheaLineGap = C.ASCENDER, C.DESCENDER, 0
    i.postscriptUnderlinePosition, i.postscriptUnderlineThickness = -100, 50
    i.openTypeNameLicense = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
    i.openTypeNameLicenseURL = "https://openfontlicense.org"

    order = []
    for g in all_glyphs():
        glyph = font.newGlyph(g.name)
        glyph.width = g.advance(p)
        if g.unicode is not None:
            glyph.unicodes = [g.unicode]
        pen = glyph.getPen()
        for contour in g.contours(p):
            draw_contour(pen, contour, p.radius)
        order.append(g.name)
    font.lib["public.glyphOrder"] = order
    return font


def write_masters(out_dir: Path) -> dict[tuple[int, int], Path]:
    """Write every master UFO into ``out_dir``; returns {(wght, rond): path}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for wght, rond in C.ALL_MASTERS:
        path = out_dir / master_filename(wght, rond)
        build_ufo(wght, rond).save(path, overwrite=True)
        paths[(wght, rond)] = path
    return paths
