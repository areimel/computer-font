"""Punctuation (! " ' ( ) , - . / : ; ? [ \\ ] _ ` { | })."""
from ..components import bar, dot, notched_rect, stem
from ..config import Params
from ..geometry import Contour, Pt, notch_corners
from ..registry import glyph


def _poly(p: Params, pts, tl: int | None = None, flip: float | None = None) -> Contour:
    """Orthogonal polygon (CCW-listed) with optional top-left step at vertex ``tl``.

    ``flip`` mirrors x about flip/2 (pass x0 + x1) so a right-hand variant of a
    left-hand outline keeps its point order; ``tl`` then names the mirrored vertex.
    """
    if flip is not None:
        pts = [(flip - x, y) for x, y in pts]
    c = Contour(tuple(Pt(*q) for q in pts))
    if tl is not None:
        c = notch_corners(c, {tl: p.notch})
    return c.oriented(True)


def _tail_dot(p: Params, x: float, y: float, h: float | None = None) -> Contour:
    """Square dot with lower-left corner (x, y) and a half-width tail hanging ``h`` below it."""
    d, h = p.dot, p.dot if h is None else h
    return _poly(p, [(x + d / 2, y - h), (x + d, y - h), (x + d, y + d), (x, y + d), (x, y), (x + d / 2, y)])


def _dot_w(p: Params) -> int:
    return p.adv(p.dot)


# ---- dots -----------------------------------------------------------------

@glyph("period", 0x2E, width=_dot_w)
def period(p: Params):
    return [dot(p, p.sb + p.dot / 2, p.dot / 2)]


@glyph("comma", 0x2C, width=_dot_w)
def comma(p: Params):
    return [_tail_dot(p, p.sb, 0)]


@glyph("colon", 0x3A, width=_dot_w)
def colon(p: Params):
    return [dot(p, p.sb + p.dot / 2, p.dot / 2), dot(p, p.sb + p.dot / 2, p.xh - p.dot / 2)]


@glyph("semicolon", 0x3B, width=_dot_w)
def semicolon(p: Params):
    return [_tail_dot(p, p.sb, 0), dot(p, p.sb + p.dot / 2, p.xh - p.dot / 2)]


@glyph("exclam", 0x21, width=_dot_w)
def exclam(p: Params):
    return [notched_rect(p, p.sb, p.dot + p.notch, p.sb + p.dot, p.cap, "tl"), dot(p, p.sb + p.dot / 2, p.dot / 2)]


@glyph("question", 0x3F, width=lambda p: p.adv(p.lc_w))
def question(p: Params):
    x0, x1 = p.sb, p.sb + p.lc_w
    s, s2, b, c = p.stem, p.stem2, p.bar, p.cap
    xs = (x0 + x1 - s) / 2
    lo, y0 = c - 3 * b, p.dot + p.notch
    hook = _poly(p, [(xs, y0), (xs + s, y0), (xs + s, lo), (x1, lo), (x1, c), (x0, c), (x0, c - b),
                     (x1 - s2, c - b), (x1 - s2, lo + b), (xs, lo + b)], tl=5)
    return [hook, dot(p, xs + s / 2, p.dot / 2)]


# ---- quotes ---------------------------------------------------------------

@glyph("quotesingle", 0x27, width=_dot_w)
def quotesingle(p: Params):
    return [_tail_dot(p, p.sb, p.cap - p.dot)]


@glyph("quotedbl", 0x22, width=lambda p: p.adv(3 * p.dot))
def quotedbl(p: Params):
    y = p.cap - p.dot
    return [_tail_dot(p, p.sb, y), _tail_dot(p, p.sb + 2 * p.dot, y)]


@glyph("grave", 0x60, width=_dot_w)
def grave(p: Params):
    return [_tail_dot(p, p.sb, p.cap - p.dot).mirrored(p.sb + p.dot / 2)]


# ---- rules ----------------------------------------------------------------

@glyph("hyphen", 0x2D, width=lambda p: p.adv(p.lc_w // 2))
def hyphen(p: Params):
    return [bar(p, p.sb, p.sb + p.lc_w // 2, p.xh / 2, align="center")]


@glyph("underscore", 0x5F, width=lambda p: p.adv(p.cap_w))
def underscore(p: Params):
    return [bar(p, 0, p.adv(p.cap_w), -p.bar)]


@glyph("bar", 0x7C, width=lambda p: p.adv(p.stem2))
def bar_(p: Params):
    return [stem(p, p.sb, p.desc, p.asc, w=p.stem2)]


# ---- brackets, parens, braces ---------------------------------------------
# Each pair is one outline; the right variant mirrors x and re-steps its top-left.

def _bracket_pts(p: Params, x0: float, x1: float, s: float):
    y0, y1, b = p.desc, p.asc, p.bar
    return [(x0, y0), (x1, y0), (x1, y0 + b), (x0 + s, y0 + b), (x0 + s, y1 - b), (x1, y1 - b), (x1, y1), (x0, y1)]


@glyph("bracketleft", 0x5B, width=lambda p: p.adv(p.stem + p.dot))
def bracketleft(p: Params):
    x0 = p.sb
    return [_poly(p, _bracket_pts(p, x0, x0 + p.stem + p.dot, p.stem), tl=7)]


@glyph("bracketright", 0x5D, width=lambda p: p.adv(p.stem2 + p.dot))
def bracketright(p: Params):
    x0 = p.sb
    x1 = x0 + p.stem2 + p.dot
    return [_poly(p, _bracket_pts(p, x0, x1, p.stem2), tl=6, flip=x0 + x1)]


def _paren_pts(p: Params, x0: float, s: float, k: float):
    """'(' outline: outer arms at x0+k, middle section bulges out to x0 (stair-stepped)."""
    y0, y1, b = p.desc, p.asc, p.bar
    h = (y1 - y0) / 4
    xs, x1 = x0 + k, x0 + k + s + p.bar
    return [(xs, y0), (x1, y0), (x1, y0 + b), (xs + s, y0 + b), (xs + s, y0 + h), (x0 + s, y0 + h),
            (x0 + s, y1 - h), (xs + s, y1 - h), (xs + s, y1 - b), (x1, y1 - b), (x1, y1), (xs, y1),
            (xs, y1 - h), (x0, y1 - h), (x0, y0 + h), (xs, y0 + h)], x1


@glyph("parenleft", 0x28, width=lambda p: p.adv(p.stem + 2 * p.bar))
def parenleft(p: Params):
    pts, _ = _paren_pts(p, p.sb, p.stem, p.bar)
    return [_poly(p, pts, tl=11)]


@glyph("parenright", 0x29, width=lambda p: p.adv(p.stem2 + 2 * p.bar))
def parenright(p: Params):
    pts, x1 = _paren_pts(p, p.sb, p.stem2, p.bar)
    return [_poly(p, pts, tl=10, flip=p.sb + x1)]


def _brace_pts(p: Params, x0: float, s: float):
    y0, y1, b = p.desc, p.asc, p.bar
    ym, xs = (y0 + y1) / 2, x0 + p.bar
    x1 = xs + s + p.bar
    return [(xs, y0), (x1, y0), (x1, y0 + b), (xs + s, y0 + b), (xs + s, y1 - b), (x1, y1 - b), (x1, y1),
            (xs, y1), (xs, ym + b / 2), (x0, ym + b / 2), (x0, ym - b / 2), (xs, ym - b / 2)], x1


@glyph("braceleft", 0x7B, width=lambda p: p.adv(p.stem + 2 * p.bar))
def braceleft(p: Params):
    pts, _ = _brace_pts(p, p.sb, p.stem)
    return [_poly(p, pts, tl=7)]


@glyph("braceright", 0x7D, width=lambda p: p.adv(p.stem2 + 2 * p.bar))
def braceright(p: Params):
    pts, x1 = _brace_pts(p, p.sb, p.stem2)
    return [_poly(p, pts, tl=6, flip=p.sb + x1)]


# ---- slashes: orthogonal stair (bottom bar, riser, top bar) ----------------

def _slash_pts(p: Params, x0: float, x1: float):
    s, b, c = p.stem, p.bar, p.cap
    xm = (x0 + x1 - s) / 2
    return [(x0, 0), (xm + s, 0), (xm + s, c - b), (x1, c - b), (x1, c), (xm, c), (xm, b), (x0, b)]


@glyph("slash", 0x2F, width=lambda p: p.adv(p.lc_w))
def slash(p: Params):
    return [_poly(p, _slash_pts(p, p.sb, p.sb + p.lc_w), tl=5)]


@glyph("backslash", 0x5C, width=lambda p: p.adv(p.lc_w))
def backslash(p: Params):
    x0, x1 = p.sb, p.sb + p.lc_w
    return [_poly(p, _slash_pts(p, x0, x1), tl=4, flip=x0 + x1)]
