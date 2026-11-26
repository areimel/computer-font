"""Basic pair kerning, written to every master UFO and scaled per master.

Values are multiples of ``p.sb`` (so they grow with weight like the sidebearings do).
Pairs are between kerning groups; each glyph sits in at most one group per side.
"""
from __future__ import annotations

from .config import Params

KERN1 = "public.kern1."  # first-glyph (left side) groups
KERN2 = "public.kern2."  # second-glyph (right side) groups

# Left-hand groups: how the first glyph's right edge behaves.
LEFT: dict[str, str] = {
    "A": "A",
    "T": "T",
    "V": "V W Y",
    "L": "L",
    "P": "P F",
    "r": "r",
}

# Right-hand groups: how the second glyph's left edge behaves.
RIGHT: dict[str, str] = {
    "A": "A",
    "T": "T",
    "V": "V W Y",
    "round": "a c d e g o q C G O Q",
    "diag": "v w y",
    "stop": "period comma",
}

# (left group, right group, kern as a multiple of p.sb). Negative = tighter.
PAIRS: tuple[tuple[str, str, float], ...] = (
    ("A", "T", -0.8), ("A", "V", -0.5),   # AT AV AW AY
    ("T", "A", -0.8), ("V", "A", -0.5),   # TA VA WA YA
    ("L", "T", -1.5), ("L", "V", -1.5),   # LT LV LW LY
    ("T", "round", -1.0), ("T", "diag", -1.0),   # To Ta Te Tw
    ("V", "round", -0.8),                 # Va Ve Vo Yo
    ("P", "A", -1.0),                     # PA FA
    ("P", "stop", -2.5), ("T", "stop", -2.0), ("V", "stop", -1.5),  # P. F. T. Y,
    ("r", "stop", -1.5), ("r", "round", -0.5),
)


def groups() -> dict[str, list[str]]:
    """UFO groups: ``public.kern1.<k>`` / ``public.kern2.<k>`` -> glyph names."""
    out = {f"{KERN1}{k}": v.split() for k, v in LEFT.items()}
    out.update({f"{KERN2}{k}": v.split() for k, v in RIGHT.items()})
    return out


def kerning(p: Params) -> dict[tuple[str, str], int]:
    """Group-pair kerning for one master location."""
    return {(KERN1 + a, KERN2 + b): round(m * p.sb) for a, b, m in PAIRS}
