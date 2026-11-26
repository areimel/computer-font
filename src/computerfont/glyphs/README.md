# Adding a glyph

Each glyph is a function `fn(p: Params) -> list[Contour]` registered with `@glyph`.
Put it in the file for its group (`uppercase.py`, `lowercase.py`, `digits.py`,
`punctuation.py`, `symbols.py`). Keep files <= ~300 lines.

```python
from ..components import frame, stem, bar, notched_rect, arch, dot
from ..config import Params
from ..geometry import polygon, Turtle, notch_corners, rect
from ..registry import glyph

@glyph("O", 0x4F, width=lambda p: p.adv(p.cap_w))   # name = AGL name, then codepoint
def O(p: Params):
    return frame(p, p.sb, 0, p.sb + p.cap_w, p.cap, outer="tl", inner="tr")
```

## Rules (these keep all masters interpolation-compatible)

1. Draw only from `Params` (never hard-code stroke sizes). Use `p.stem` (vertical
   strokes, heavy), `p.bar` (horizontal, thinner), `p.notch`, `p.dot`, `p.sb`
   (sidebearing), `p.cap`, `p.xh`, `p.asc`, `p.desc`, `p.cap_w`, `p.lc_w`.
2. The vertex count and order of every contour must NOT depend on `wght`/`rond`
   (no `if p.wght > 500`). `tests/test_compat.py` enforces this for every glyph.
3. Draw in absolute coordinates, baseline y=0, left edge of the drawing box at `p.sb`.
   Advance width = `p.adv(box_width)` (adds both sidebearings), or a fixed int.
4. Outer contours CCW, counters CW. Builders already do this; for hand-made counters
   call `.counter()`. `polygon(...)` / `Turtle.close()` normalise orientation for you.
5. Overlap joined strokes (never merely touch). Overlaps are kept, not merged.
   Prefer one polygon per connected shape if you want inner corners rounded too.
6. Corner rounding is automatic (every vertex -> a cubic, radius = ROND% of half
   the stem, clamped to half of each adjacent edge). Mark vertices that must never
   round with `sharp` (`Turtle.h(dx, sharp=True)`; notch inner corners already are).

## Building blocks

- `geometry`: `Pt`, `Contour(pts, sharp)` with `.translated(dx,dy) .mirrored(axis_x)
  .flipped(axis_y) .reversed() .counter() .oriented(ccw) .area`; `rect(x0,y0,x1,y1)`;
  `polygon((x,y),...)`; `Turtle(x,y).h(dx).v(dy).to(x,y).close(counter=False)`;
  `notch_corners(contour, {vertex_index: size})` cuts a square step at a vertex
  (works on concave vertices too, adding material).
- `components`: `stem(p, x, y0, y1, w=None)`, `bar(p, x0, x1, y, t=None, align="bottom|top|center")`,
  `notched_rect(p, x0,y0,x1,y1, corners="tl br", n=None)`,
  `frame(p, x0,y0,x1,y1, outer="tl", inner="tr", sides=None, bars=None)` -> [outer, counter],
  `arch(p, x0, x1, y1, outer="tl", inner="tr")` (n shape), `dot(p, cx, cy, size=None)`.
  Corner names: `"tl" "tr" "bl" "br"`, space-separated for several.
- Need a shape used by 3+ glyphs? Add it to `components.py` (generic, Params-driven).

## Example: a stem + bar glyph (T-like)

```python
@glyph("T", 0x54, width=lambda p: p.adv(p.cap_w))
def T(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w
    cx = (x0 + x1 - p.stem) / 2
    return [bar(p, x0, x1, p.cap, align="top"), stem(p, cx, 0, p.cap - p.bar // 2)]
```

Glyph names must be standard AGL names (`A`, `a`, `zero`, `period`, `comma`,
`exclam`, ...). Check your work: `PYTHONPATH=src .venv/bin/python -m pytest -q`, then
`PYTHONPATH=src .venv/bin/python -m computerfont.build`.
