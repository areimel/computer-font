"""Fast glyph preview straight from the parametric source (no fontmake build).

Usage:
    PYTHONPATH=src .venv/bin/python scripts/render_glyphs.py "ABC" out.png
    PYTHONPATH=src .venv/bin/python scripts/render_glyphs.py --all out.png

Renders the given characters at every master location (rows) so weight and
corner-radius behaviour can be eyeballed. Requires freetype-py.
"""
from __future__ import annotations

import argparse

from fontTools.pens.freetypePen import FreeTypePen
from PIL import Image, ImageDraw

from computerfont.config import ALL_MASTERS, Params
from computerfont.corners import draw_contour
from computerfont.registry import all_glyphs

SCALE = 0.12  # px per font unit
PAD = 12
LABEL_W = 110


def glyph_image(gdef, p: Params) -> Image.Image:
    """Rasterise one glyph at Params ``p`` as a white-on-transparent PIL image."""
    pen = FreeTypePen(None)
    for contour in gdef.contours(p):
        draw_contour(pen, contour, p.radius, ndigits=None)
    w = max(1, int(gdef.advance(p) * SCALE))
    h = int((p.asc - p.desc) * SCALE)
    return pen.image(width=w, height=h, transform=(SCALE, 0, 0, SCALE, 0, -p.desc * SCALE), contain=False)


def render(chars: list, out: str) -> None:
    rows = []
    for wght, rond in sorted(ALL_MASTERS):
        p = Params.at(wght, rond)
        rows.append((f"w{wght} r{rond}", [glyph_image(g, p) for g in chars]))
    row_h = max(im.height for _, ims in rows for im in ims) + PAD
    width = LABEL_W + max(sum(im.width + PAD for im in ims) for _, ims in rows)
    sheet = Image.new("L", (width, row_h * len(rows)), 255)
    draw = ImageDraw.Draw(sheet)
    for i, (label, ims) in enumerate(rows):
        y = i * row_h
        draw.text((4, y + row_h // 2), label, fill=0)
        x = LABEL_W
        for im in ims:
            sheet.paste(0, (x, y), im.getchannel("A"))
            x += im.width + PAD
    sheet.save(out)
    print(f"wrote {out}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("chars", nargs="?", default="", help="characters to render")
    ap.add_argument("out", help="output PNG path")
    ap.add_argument("--all", action="store_true", help="render every registered glyph")
    a = ap.parse_args()
    glyphs = all_glyphs()
    if not a.all:
        by_cp = {g.unicode: g for g in glyphs if g.unicode is not None}
        glyphs = [by_cp[ord(c)] for c in a.chars if ord(c) in by_cp]
    render(glyphs, a.out)


if __name__ == "__main__":
    main()
