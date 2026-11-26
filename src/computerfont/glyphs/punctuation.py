"""Punctuation (! " ' ( ) , - . / : ; ? [ ] _ { | } etc.)."""
from ..components import dot
from ..config import Params
from ..registry import glyph


@glyph("period", 0x2E, width=lambda p: p.adv(p.dot))
def period(p: Params):
    return [dot(p, p.sb + p.dot / 2, p.dot / 2)]
