"""Designspace: 2 axes (wght, ROND), masters, named instances."""
from __future__ import annotations

from pathlib import Path

from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, InstanceDescriptor, SourceDescriptor

from . import config as C
from .ufo import master_filename


def build_designspace(ufo_dir: Path) -> DesignSpaceDocument:
    doc = DesignSpaceDocument()
    for ax in C.AXES:
        doc.addAxis(
            AxisDescriptor(
                tag=ax.tag, name=ax.name, minimum=ax.minimum, default=ax.default, maximum=ax.maximum
            )
        )
    for wght, rond in C.ALL_MASTERS:
        doc.addSource(
            SourceDescriptor(
                path=str(ufo_dir / master_filename(wght, rond)),
                familyName=C.FAMILY_NAME,
                styleName=C.style_name(wght, rond),
                location={"Weight": wght, "Roundness": rond},
            )
        )
    for style, wght, rond in C.INSTANCES:
        doc.addInstance(
            InstanceDescriptor(
                familyName=C.FAMILY_NAME,
                styleName=style,
                postScriptFontName=f"{C.FILE_STEM}-{style.replace(' ', '')}",
                styleMapFamilyName=f"{C.FAMILY_NAME} {style}",
                styleMapStyleName="regular",
                location={"Weight": wght, "Roundness": rond},
            )
        )
    return doc


def write_designspace(out_dir: Path) -> Path:
    """Write ``<out_dir>/ComputerFont.designspace`` (UFOs expected beside it)."""
    path = out_dir / f"{C.FILE_STEM}.designspace"
    build_designspace(out_dir).write(path)
    return path
