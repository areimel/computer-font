"""Symbols: # $ % & * + < = > @ ^ ~ (AGL names numbersign ... asciitilde)."""
from ..components import bar, dot, frame, notched_rect, stem
from ..config import Params
from ..geometry import Contour, polygon, rect
from ..registry import glyph


# ---- private helpers (components.py candidates) -------------------------------------------
def _mid(p: Params) -> int:
    """Math axis: vertical middle of the x-height."""
    return p.xh // 2


def _diag(x0: float, y0: float, x1: float, y1: float, t: float) -> Contour:
    """Slanted stroke from bottom (x0,y0) to top (x1,y1), horizontal thickness t (4 fixed vertices)."""
    return polygon((x0, y0), (x0 + t, y0), (x1 + t, y1), (x1, y1))


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


def _s_shape(p: Params, x0: float, y0: float, x1: float, y1: float) -> Contour:
    """Blocky S in one 12-point polygon: top bar, left upper stem, middle bar, right lower stem, bottom bar."""
    s, s2, b = p.stem, p.stem2, p.bar
    lo = (y0 + y1 - b) // 2
    hi = lo + b
    return polygon(
        (x0, y1), (x1, y1), (x1, y1 - b), (x0 + s, y1 - b), (x0 + s, hi), (x1, hi),
        (x1, y0), (x0, y0), (x0, y0 + b), (x1 - s2, y0 + b), (x1 - s2, lo), (x0, lo),
    )


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
    return [_s_shape(p, x0, 0, x1, p.cap), stem(p, cx, -ext, p.cap + ext, p.stem2)]


@glyph("percent", 0x25, width=lambda p: p.adv(p.cap_w + p.cap_w // 4))
def percent(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w + p.cap_w // 4
    w = 2 * p.stem2 + 2 * p.notch  # small ring: thin walls, square-ish counter
    h = 2 * p.bar + 2 * p.notch
    return [
        *frame(p, x0, p.cap - h, x0 + w, p.cap, outer="tl", sides=p.stem2),
        *frame(p, x1 - w, 0, x1, h, sides=p.stem2),
        _diag(x0 + w // 2, 0, x1 - w // 2 - p.stem, p.cap, p.stem),
    ]


@glyph("ampersand", 0x26, width=lambda p: p.adv(p.cap_w))
def ampersand(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w
    split = p.cap * 5 // 12  # top of the big lower bowl
    ux1 = x1 - p.stem - p.notch  # the upper bowl is narrower than the lower one
    return [
        *frame(p, x0, 0, x1, split + p.bar, outer="tl"),
        *frame(p, x0, split, ux1, p.cap, outer="tl"),
        stem(p, x1 - p.stem2, split, p.cap - 2 * p.bar, p.stem2),  # detached right arm, gap above
    ]


@glyph("asterisk", 0x2A, width=lambda p: p.adv(p.lc_w))
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


@glyph("plus", 0x2B, width=lambda p: p.adv(p.lc_w))
def plus(p: Params):
    r = p.lc_w // 2
    return [_cross(p.sb + r, _mid(p), r, r, p.stem2, p.bar)]


@glyph("less", 0x3C, width=lambda p: p.adv(p.lc_w))
def less(p: Params):
    return [_chevron(p.sb, p.sb + p.lc_w, _mid(p), p.lc_w // 2, p.stem)]


@glyph("equal", 0x3D, width=lambda p: p.adv(p.lc_w))
def equal(p: Params):
    x0, x1, cy = p.sb, p.sb + p.lc_w, _mid(p)
    return [
        notched_rect(p, x0, cy + p.bar // 2, x1, cy + p.bar // 2 + p.bar, "tl"),
        bar(p, x0, x1, cy - p.bar // 2, align="top"),
    ]


@glyph("greater", 0x3E, width=lambda p: p.adv(p.lc_w))
def greater(p: Params):
    c = _chevron(p.sb, p.sb + p.lc_w, _mid(p), p.lc_w // 2, p.stem)
    return [c.mirrored(p.sb + p.lc_w / 2)]


@glyph("at", 0x40, width=lambda p: p.adv(p.cap_w + p.cap_w // 4))
def at(p: Params):
    x0, x1 = p.sb, p.sb + p.cap_w + p.cap_w // 4
    g = p.bar  # channel between the outer frame and the inner ring
    ix0, iy1 = x0 + p.stem + g, p.cap - p.bar - g
    return [
        *frame(p, x0, 0, x1, p.cap, outer="tl", inner="tr"),
        # inner ring fused to the outer right/bottom walls (overlapping them)
        *frame(p, ix0, p.bar // 2, x1 - p.stem2 // 2, iy1, sides=p.stem2),
    ]


@glyph("asciicircum", 0x5E, width=lambda p: p.adv(p.lc_w))
def asciicircum(p: Params):
    x0, x1, cx = p.sb, p.sb + p.lc_w, p.sb + p.lc_w // 2
    top, y0, v = p.cap, p.cap - p.lc_w // 2, p.bar
    return [polygon((x0, y0), (cx, top), (x1, y0), (x1, y0 - v), (cx, top - v), (x0, y0 - v))]


@glyph("asciitilde", 0x7E, width=lambda p: p.adv(p.lc_w))
def asciitilde(p: Params):
    x0, x1, w = p.sb, p.sb + p.lc_w, p.lc_w // 3
    base, h, v = _mid(p) - p.bar, p.lc_w // 3, p.bar
    top = [(x0, base + h // 2), (x0 + w, base + h), (x0 + 2 * w, base), (x1, base + h // 2)]
    return [polygon(*top, *[(x, y + v) for x, y in reversed(top)])]
