"""Glyph registry: ``@glyph("H", 0x48, width=...)`` registers a drawing function."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union

from .config import Params
from .geometry import Contour

Draw = Callable[[Params], list[Contour]]
Width = Union[int, Callable[[Params], int]]


@dataclass(frozen=True)
class GlyphDef:
    name: str
    unicode: int | None
    width: Width
    draw: Draw

    def advance(self, p: Params) -> int:
        return self.width(p) if callable(self.width) else self.width

    def contours(self, p: Params) -> list[Contour]:
        return self.draw(p)


_REGISTRY: dict[str, GlyphDef] = {}


def glyph(name: str, unicode: int | None, width: Width) -> Callable[[Draw], Draw]:
    """Register ``fn(p: Params) -> list[Contour]``. ``width`` is an int or ``fn(p) -> int``."""

    def deco(fn: Draw) -> Draw:
        if name in _REGISTRY:
            raise ValueError(f"glyph {name!r} registered twice")
        _REGISTRY[name] = GlyphDef(name, unicode, width, fn)
        return fn

    return deco


def all_glyphs() -> list[GlyphDef]:
    """All glyphs in registration order, with .notdef first and space second."""
    import computerfont.glyphs  # noqa: F401  (triggers registration)

    defs = list(_REGISTRY.values())
    rank = {".notdef": 0, "space": 1}
    return sorted(defs, key=lambda g: (rank.get(g.name, 2), g.unicode or 0))


def get(name: str) -> GlyphDef:
    all_glyphs()
    return _REGISTRY[name]
