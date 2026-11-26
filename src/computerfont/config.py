"""Single source of truth: names, metrics, axes, masters, and per-location Params."""
from __future__ import annotations

from dataclasses import dataclass

FAMILY_NAME = "Computer Font"
FILE_STEM = FAMILY_NAME.replace(" ", "")  # "ComputerFont"
VERSION = (0, 100)  # major, minor-thousandths -> "Version 0.100"
UPM = 1000
CAP_HEIGHT = 700
X_HEIGHT = 540
ASCENDER = 760
DESCENDER = -220

STEM_CONTRAST = 0.6  # stem2 / stem: right stems are thinner than left stems
CAP_BOX_W = 560  # outer width of a capital's drawing box (before sidebearings)
LC_BOX_W = 480  # outer width of a lowercase drawing box


@dataclass(frozen=True)
class Axis:
    tag: str
    name: str
    minimum: int
    default: int
    maximum: int


AXES = (Axis("wght", "Weight", 200, 400, 900), Axis("ROND", "Roundness", 0, 0, 100))

# The four corner masters (wght x ROND). The default wght (400) must coincide with
# a source for fontmake, and without a (400, 100) master ROND would do nothing at
# wght 400 (sparse masters), so the 400 column is added: 6 masters in a 3x2 grid.
MASTERS: tuple[tuple[int, int], ...] = ((200, 0), (900, 0), (200, 100), (900, 100))
DEFAULT_MASTER = (400, 0)
ALL_MASTERS = (DEFAULT_MASTER, (400, 100), *MASTERS)

WEIGHT_NAMES = {200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium", 700: "Bold", 900: "Black"}
INSTANCE_WEIGHTS = tuple(WEIGHT_NAMES)  # ExtraLight..Black
INSTANCE_ROUNDS = (0, 100)  # Sharp, Round


def style_name(wght: int, rond: int) -> str:
    """'Bold' for sharp, 'Round Bold' for fully round; partial values get 'R<n>'."""
    base = WEIGHT_NAMES.get(wght, f"W{wght}")
    if rond == 0:
        return base
    return f"Round {base}" if rond == 100 else f"R{rond} {base}"


INSTANCES: tuple[tuple[str, int, int], ...] = tuple(
    (style_name(w, r), w, r) for r in INSTANCE_ROUNDS for w in INSTANCE_WEIGHTS
)

VF_NAME = f"{FILE_STEM}[wght,ROND].ttf"


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


@dataclass(frozen=True)
class Params:
    """Design parameters at one (wght, rond) location. All lengths in font units.

    Every dimension is linear in wght so masters interpolate exactly.
    """

    wght: int
    rond: int
    stem: int  # primary (left) vertical stroke thickness (heavy)
    stem2: int  # secondary (right) vertical stroke: the style's left-heavy contrast
    bar: int  # horizontal stroke thickness (thinner)
    notch: int  # size of the square corner steps
    radius: int  # target corner radius (clamped per corner later)
    sb: int  # sidebearing
    dot: int  # square dot / period size
    cap: int = CAP_HEIGHT
    xh: int = X_HEIGHT
    asc: int = ASCENDER
    desc: int = DESCENDER
    cap_w: int = CAP_BOX_W
    lc_w: int = LC_BOX_W

    @classmethod
    def at(cls, wght: int, rond: int = 0) -> "Params":
        t = (wght - 200) / 700
        stem = _lerp(54, 160, t)
        return cls(
            wght=wght,
            rond=rond,
            stem=round(stem),
            stem2=round(stem * STEM_CONTRAST),
            bar=round(_lerp(38, 120, t)),
            notch=round(_lerp(22, 44, t)),
            radius=round(stem / 2 * rond / 100),
            sb=round(_lerp(40, 60, t)),
            dot=round(_lerp(70, 170, t)),
        )

    def adv(self, box_w: int) -> int:
        """Advance width for a drawing box of width ``box_w``."""
        return box_w + 2 * self.sb
