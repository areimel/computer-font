"""Symbols: # $ % & * + < = > @ ^ ~ (AGL names numbersign ... asciitilde)."""
from ..components import bar, diag as _diag, frame, lc_width, math_axis, notched_poly, notched_rect, s_shape, stem
from ..config import Params
from ..geometry import Contour, polygon, rect
from ..registry import glyph


# ---- private helpers (each used by only 1-2 glyphs here) -----------------------------------
def _cross(cx: float, cy: float, rx: float, ry: float, v: float, h: float) -> Contour:
    """Plus-shaped polygon: arms reach rx/ry from the centre; vertical arm width v, horizontal thickness h."""
    a, b = v / 2, h / 2
    return polygon(
        (cx - a, cy - ry), (cx + a, cy - ry), (cx + a, cy - b), (cx + rx, cy - b), (cx + rx, cy + b),
        (cx + a, cy + b), (cx + a, cy + ry), (cx - a, cy + ry), (cx - a, cy + b), (cx - rx, cy + b),
        (cx - rx, cy - b), (cx - a, cy - b),
    )


def _chevron(x0: float, x1: float, cy: float, h: float, t: float) -> Contour:
    """'<' pointing left: tip at (x0, cy), arms rise/fall by h to x1, horizontal thickness t."""
    return polygon((x0, cy), (x1 - t, cy + h), (x1, cy + h), (x0 + t, cy), (x1, cy - h), (x1 - t, cy - h))


# ---- glyphs -------------------------------------------------------------------------------
@glyph("numbersign", 0x23, width=lambda p: p.adv(p.cap_w))
def numbersign(p: Params):
    x0, x1, t = p.sb, p.sb + p.cap_w, p.stem2
    gx, gy = (p.cap_w - 2 * t) // 3, (p.cap - 2 * p.bar) // 3
    out = [stem(p, x0 + gx // 2 + k * (gx + t), 0, p.cap, t) for k in (0, 1)]
    out += [bar(p, x0, x1, gy * (k + 1) + p.bar * k - p.bar // 2) for k in (0, 1)]
    return out


@glyph("dollar", 0x24, width=lambda p: p.adv(p.cap_w))
def dollar(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w
    cx = (x0 + x1 - p.stem2) / 2
    ext = p.bar  # the vertical stem pokes out above and below the S
    return [s_shape(p, x0, 0, x1, p.cap), stem(p, cx, -ext, p.cap + ext, p.stem2)]


@glyph("percent", 0x25, width=lambda p: p.adv(p.cap_w + p.cap_w // 4))
def percent(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w + p.cap_w // 4
    w = 2 * p.stem2 + p.cap // 7  # small rings, about a third of the height
    h = 2 * p.bar + p.cap // 8
    return [
        *frame(p, x0, p.cap - h, x0 + w, p.cap, outer="tl", sides=p.stem2),
        *frame(p, x1 - w, 0, x1, h, sides=p.stem2),
        _diag(x0 + w // 2, 0, x1 - w // 2 - p.stem, p.cap, p.stem),
    ]


def _amp_w(p: Params) -> int:
    return p.cap_w + p.stem2 + 2 * p.notch  # bowl box plus the spur reaching out to the right


@glyph("ampersand", 0x26, width=lambda p: p.adv(_amp_w(p)))
def ampersand(p: Params):
    x0, xb = p.sb, p.sb + p.cap_w
    x1 = p.sb + _amp_w(p)
    split = p.cap * 5 // 12  # top of the big lower bowl
    ux1 = x0 + p.cap_w * 2 // 3  # the upper loop is narrower than the bowl
    yl = split - p.bar
    spur = notched_poly(p, [(xb - p.stem2, yl), (x1, yl), (x1, yl + 3 * p.bar), (x1 - p.stem2, yl + 3 * p.bar),
                            (x1 - p.stem2, yl + p.bar), (xb - p.stem2, yl + p.bar)], tl=2)
    return [*frame(p, x0, 0, xb, split + p.bar, outer="tl"), *frame(p, x0, split, ux1, p.cap, outer="tl"), spur]


@glyph("asterisk", 0x2A, width=lc_width)
def asterisk(p: Params):
    cx, r = p.sb + p.lc_w // 2, p.lc_w // 2
    cy = p.cap - r
    t = p.stem2
    return [
        rect(cx - t / 2, cy - r, cx + t / 2, cy + r),
        rect(cx - r, cy - p.bar / 2, cx + r, cy + p.bar / 2),
        _diag(cx - r + t // 2, cy - r, cx + r - t - t // 2, cy + r, t),
        _diag(cx - r + t // 2, cy + r, cx + r - t - t // 2, cy - r, t),
    ]


@glyph("plus", 0x2B, width=lc_width)
def plus(p: Params):
    r = p.lc_w // 2
    return [_cross(p.sb + r, math_axis(p), r, r, p.stem2, p.bar)]


@glyph("less", 0x3C, width=lc_width)
def less(p: Params):
    return [_chevron(p.sb, p.sb + p.lc_w, math_axis(p), p.lc_w // 2, p.stem)]


@glyph("equal", 0x3D, width=lc_width)
def equal(p: Params):
    x0, x1, cy = p.sb, p.sb + p.lc_w, math_axis(p)
    return [
        notched_rect(p, x0, cy + p.bar // 2, x1, cy + p.bar // 2 + p.bar, "tl"),
        bar(p, x0, x1, cy - p.bar // 2, align="top"),
    ]


@glyph("greater", 0x3E, width=lc_width)
def greater(p: Params):
    c = _chevron(p.sb, p.sb + p.lc_w, math_axis(p), p.lc_w // 2, p.stem)
    return [c.mirrored(p.sb + p.lc_w / 2)]


@glyph("at", 0x40, width=lambda p: p.adv(p.cap_w + p.cap_w // 4))
def at(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w + p.cap_w // 4
    s, s2, b, g, c = p.stem, p.stem2, p.bar, p.notch, p.cap
    # outer C: closed top and left, right wall stops short of the bottom bar (open tail slot)
    outer = notched_poly(p, [(x0, 0), (x1, 0), (x1, b), (x1 - s2, b), (x0 + s, b), (x0 + s, c - b), (x1 - s2, c - b),
                             (x1 - s2, 2 * b + g), (x1, 2 * b + g), (x1, c), (x0, c)], tl=10)
    # inner 'a': top bar, mid bar, right stem, bottom bar, left stem below the mid bar
    ix0, ix1, iy0, iy1 = x0 + s + b, x1 - s2 + g, b // 2, c - 2 * b
    lo = iy0 + (iy1 - iy0 - b) // 2
    inner = notched_poly(p, [(ix0, iy0), (ix1, iy0), (ix1, iy1), (ix0, iy1), (ix0, iy1 - b), (ix1 - s2, iy1 - b),
                             (ix1 - s2, lo + b), (ix0, lo + b)], tl=3)
    return [outer, inner, notched_rect(p, ix0 + s2, iy0 + b, ix1 - s2, lo, "tr").counter()]


@glyph("asciicircum", 0x5E, width=lc_width)
def asciicircum(p: Params):
    x0, x1, cx = p.sb, p.sb + p.lc_w, p.sb + p.lc_w // 2
    top, y0, v = p.cap, p.cap - p.lc_w // 2, p.bar
    return [polygon((x0, y0), (cx, top), (x1, y0), (x1, y0 - v), (cx, top - v), (x0, y0 - v))]


@glyph("asciitilde", 0x7E, width=lc_width)
def asciitilde(p: Params):
    x0, x1, w = p.sb, p.sb + p.lc_w, p.lc_w // 3
    base, h, v = math_axis(p) - p.bar, p.lc_w // 3, p.bar
    top = [(x0, base + h // 2), (x0 + w, base + h), (x0 + 2 * w, base), (x1, base + h // 2)]
    return [polygon(*top, *[(x, y + v) for x, y in reversed(top)])]
