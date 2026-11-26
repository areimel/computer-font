"""CLI: generate UFOs + designspace, run fontmake, make woff2.

    python -m computerfont.build [--static] [--root DIR]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

from . import config as C
from .designspace import write_designspace
from .ufo import write_masters


def _fontmake(*args: str) -> None:
    subprocess.run([sys.executable, "-m", "fontmake", *args], check=True)


def build_variable(ds: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ttf = out_dir / C.VF_NAME
    _fontmake("-m", str(ds), "-o", "variable", "--keep-overlaps", "--output-path", str(ttf))
    return ttf


def make_woff2(ttf: Path) -> Path:
    font = TTFont(ttf)
    font.flavor = "woff2"
    out = ttf.with_suffix(".woff2")
    font.save(out)
    return out


def build_static(ds: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    _fontmake("-m", str(ds), "-i", "-o", "ttf", "--keep-overlaps", "--output-dir", str(out_dir))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--static", action="store_true", help="also build static TTF instances")
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="repo root (default: cwd)")
    args = ap.parse_args(argv)

    gen = args.root / "sources" / "generated"
    if gen.exists():
        shutil.rmtree(gen)
    write_masters(gen)
    ds = write_designspace(gen)
    ttf = build_variable(ds, args.root / "fonts" / "variable")
    print("built", ttf, "and", make_woff2(ttf))
    if args.static:
        build_static(ds, args.root / "fonts" / "static")


if __name__ == "__main__":
    main()
