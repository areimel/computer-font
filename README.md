# Computer Font

<!-- specimen image -->

Computer Font is a parametric, open-source display typeface inspired by blocky 1970s computer lettering. Every glyph is drawn in code as an orthogonal polygon, so the same design can be regenerated at any weight and corner radius. The project builds a single variable OpenType font from Python sources, with no hand-drawn outlines and no copied artwork.

## Features

- **Two variation axes:** `wght` (200 Thin to 900 Black) and `ROND` (0 sharp to 100 fully rounded corners), with named instances from Thin to Black in Sharp and Round styles.
- **ASCII character set:** printable ASCII (U+0020 to U+007E), 95 glyphs plus `.notdef`.
- **Open license:** the font is released under the SIL Open Font License 1.1, and the build code under MIT.
- **Reproducible builds:** Python generates UFO masters, and fontmake compiles a variable TTF and WOFF2.

## Building

Requires Python 3.11 or newer.

```sh
make setup    # create .venv and install dependencies (editable install)
make build    # generate UFO masters and compile fonts into fonts/
make test     # run the pytest suite
make proof    # render a weight x radius specimen grid into proofs/
```

Other targets:

- `make reference` downloads the original font for visual comparison (see below).
- `make clean` removes `build/`, `fonts/`, `sources/generated/`, and `proofs/`.

## Project layout

```
computer-font/
  README.md  CLAUDE.md  OFL.txt  LICENSE-CODE  AUTHORS.txt  CHANGELOG.md
  .gitignore  requirements.txt  Makefile  pyproject.toml
  docs/superpowers/specs/2026-11-26-computer-font-design.md
  scripts/fetch_reference.sh          # downloads original into reference/ (gitignored)
  src/computerfont/
    config.py        # family name, UPM, metrics, axis ranges, master parameters
    geometry.py      # points, polygons, orthogonal path builder helpers
    corners.py       # compatible corner rounding (degenerate at radius 0)
    components.py    # reusable parts: stem, bar, bowl, notch, dot, tail, comma
    registry.py      # @glyph decorator and lookup
    glyphs/          # uppercase.py lowercase.py digits.py punctuation.py symbols.py
    ufo.py           # draws the registry into a ufoLib2 font per master
    designspace.py   # two axes, four masters, named instances
    build.py         # CLI: UFOs -> variable TTF, WOFF2, static instances
    proof.py         # PNG specimen across the axis grid
  tests/             # geometry, corners, master compatibility, charset
  specimen/index.html  # browser test page with wght and ROND sliders
  build/ fonts/ sources/generated/ reference/ proofs/   # generated, gitignored
```

## How glyphs are drawn

Each glyph is an **orthogonal polygon**: a list of vertices whose coordinates are expressions of shared metrics such as stem width, notch depth, and cap height. Boolean operations are never used, so the point structure of a glyph does not change between masters.

Every corner is emitted as a cubic curve with two off-curve handles. At radius 0 the handles sit on the corner, so sharp outlines remain structurally compatible with rounded ones. The radius of each corner is clamped so it fits its adjacent edges.

The variable font interpolates between four masters: `wght` at 200 and 900, crossed with `ROND` at 0 and 100. `ROND` is a percentage of the maximum radius, which is half the local stem.

## Reference

`make reference` runs `scripts/fetch_reference.sh`, which downloads the original 1992 display face into the gitignored `reference/` folder. It is used only for visual comparison while drawing. The original file is never committed or redistributed. Its license is unknown, and the outlines in this project are an independent redraw.

## License

- **Fonts:** SIL Open Font License 1.1. See [OFL.txt](OFL.txt).
- **Build code:** MIT. See [LICENSE-CODE](LICENSE-CODE).

Copyright 2026 The Computer Font Project Authors. Authors are listed in [AUTHORS.txt](AUTHORS.txt).
