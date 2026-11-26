"""Specimen PNGs for the variable font: a wght x ROND grid and a size waterfall.

Run ``make build`` first, then ``make proof``. Writes proofs/grid.png and proofs/waterfall.png.
"""
from __future__ import annotations

import math
from io import BytesIO
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont

from computerfont import config

ROOT = Path(__file__).resolve().parents[2]
VF_PATH = ROOT / "fonts" / "variable" / config.VF_NAME
PROOFS_DIR = ROOT / "proofs"

WGHTS = (200, 400, 700, 900)
ROUNDS = (0, 50, 100)
GRID_SIZE = 36  # px, ASCII rows in the grid
ASCII_LINES = 3
ASCII = "".join(chr(c) for c in range(0x21, 0x7F))  # printable ASCII, no space
WATERFALL_TEXT = "The quick brown fox jumps over the lazy dog 0123456789"
WATERFALL_SIZES = (12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 56, 64, 72, 80, 96)

BG = (255, 255, 255)
FG = (20, 20, 20)
LABEL_FG = (120, 120, 120)
RULE = (225, 225, 225)
PAD = 24
GAP = 10

# One text row: (font, text, colour). Every image in this module is built from these.
Row = tuple[ImageFont.FreeTypeFont, str, tuple[int, int, int]]


def load_vf() -> TTFont:
    if not VF_PATH.exists():
        raise SystemExit(f"Missing variable font: {VF_PATH}\nRun `make build` first.")
    return TTFont(VF_PATH)


def default_location() -> dict[str, float]:
    return {axis.tag: axis.default for axis in config.AXES}


def instance_bytes(vf: TTFont, location: dict[str, float]) -> bytes:
    """Pin the axes at ``location`` and return the static font as TTF bytes (in memory)."""
    static = instancer.instantiateVariableFont(vf, location)  # inplace=False: vf is untouched
    buf = BytesIO()
    static.save(buf)
    return buf.getvalue()


def font_at(data: bytes, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BytesIO(data), size)


def label_font() -> ImageFont.FreeTypeFont:
    return ImageFont.load_default(size=18)  # Pillow's built-in face, so labels never depend on our glyphs


def ascii_lines(n: int = ASCII_LINES) -> list[str]:
    step = math.ceil(len(ASCII) / n)
    return [ASCII[i : i + step] for i in range(0, len(ASCII), step)]


def render_rows(rows: list[Row], bg: tuple[int, int, int] = BG) -> Image.Image:
    """The single render helper: stack text rows top to bottom on one background."""
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    metrics = []
    for font, text, _ in rows:
        ascent, descent = font.getmetrics()
        metrics.append((math.ceil(probe.textlength(text, font=font)), ascent + descent))
    width = max(w for w, _ in metrics) + 2 * PAD
    height = sum(h for _, h in metrics) + GAP * (len(rows) - 1) + 2 * PAD
    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    y = PAD
    for (font, text, colour), (_, h) in zip(rows, metrics):
        draw.text((PAD, y), text, font=font, fill=colour)
        y += h + GAP
    return img


def build_grid(vf: TTFont) -> Image.Image:
    """wght (rows) x ROND (columns), each cell a label plus the ASCII set."""
    cells: list[list[Image.Image]] = []
    for wght in WGHTS:
        row = []
        for rond in ROUNDS:
            font = font_at(instance_bytes(vf, {"wght": wght, "ROND": rond}), GRID_SIZE)
            rows: list[Row] = [(label_font(), f"wght {wght}   ROND {rond}", LABEL_FG)]
            rows += [(font, line, FG) for line in ascii_lines()]
            row.append(render_rows(rows))
        cells.append(row)
    return _tile(cells)


def _tile(cells: list[list[Image.Image]]) -> Image.Image:
    cw = max(im.width for row in cells for im in row)
    ch = max(im.height for row in cells for im in row)
    out = Image.new("RGB", (len(cells[0]) * cw, len(cells) * ch), BG)
    draw = ImageDraw.Draw(out)
    for r, row in enumerate(cells):
        for c, im in enumerate(row):
            x, y = c * cw, r * ch
            out.paste(im, (x, y))
            draw.rectangle([x, y, x + cw - 1, y + ch - 1], outline=RULE)
    return out


def build_waterfall(vf: TTFont) -> Image.Image:
    """The sample sentence at each size in WATERFALL_SIZES, default instance."""
    font_data = instance_bytes(vf, default_location())
    rows: list[Row] = []
    for size in WATERFALL_SIZES:
        rows.append((label_font(), f"{size} px", LABEL_FG))
        rows.append((font_at(font_data, size), WATERFALL_TEXT, FG))
    return render_rows(rows)


def main() -> None:
    vf = load_vf()
    PROOFS_DIR.mkdir(exist_ok=True)
    grid_path = PROOFS_DIR / "grid.png"
    waterfall_path = PROOFS_DIR / "waterfall.png"
    build_grid(vf).save(grid_path)
    build_waterfall(vf).save(waterfall_path)
    print(f"wrote {grid_path}")
    print(f"wrote {waterfall_path}")


if __name__ == "__main__":
    main()
