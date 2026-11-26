# Computer Font — project setup & v1 build plan

## Context
The user wants their own open-source (OFL) take on dafont's "Computerfont" (Fontographer 3.5, 1992; no author or license info anywhere). It's a blocky, notched, 1970s "computer" display face. Recon of the original's 194 glyphs found:
- 8 icon glyphs to drop: Mac computers (Á Ê Ë), rockets (Â Í), starship (È, ‰), floppy (Î), R2-D2 (Ÿ).
- Gaps and broken glyphs across Latin-1, which are out of scope for v1.

**Decisions (user):** OFL open-source release · parametric code-drawn glyphs · v1 charset = **printable ASCII only (U+0020–007E, 95 glyphs + .notdef)** · variable axes = **Weight (`wght`) + Corner radius (`ROND`)**. Repo is public on GitHub as `areimel/computer-font` (gh is authenticated).

**Why parametric redraw:** each glyph is an orthogonal polygon of strokes and notches, so code can regenerate it at any weight or radius. We never copy the original outlines, whose license is unknown. The original TTF is fetched only into a gitignored `reference/` folder as a visual guide and is never committed.

**Non-goals (v1):** Latin-1 accents and symbols, width axis, hinting, Google Fonts submission. **Anti-goals:** any icon/pictogram glyphs; reusing the original's outline data; one huge glyph file.

**Working family name:** "Computer Font". It's set in a single config constant so a rename takes one line. Flag it at the end, since it's close to the original "Computerfont".

## Design
**Toolchain:** Python 3.12+ venv, `fonttools`, `ufoLib2`, `fontmake` (ufo2ft), `skia-pathops` (only if needed), `pytest`, `pillow` (proofs). The Makefile wraps everything: `make setup|build|test|proof|clean`.

**Interpolation strategy (the key constraint):** all masters must have identical point structure.
- Glyphs are defined as **orthogonal polygons**, meaning vertex lists whose coordinates are expressions of shared metrics (stem width, notch depth, cap height…). Boolean ops are not used, so the structure never changes between masters.
- Every corner is always emitted as a cubic curve (on, off, off, on). At radius 0 the handles collapse onto the corner, so the sharp masters stay compatible with the round ones.
- The radius is clamped per corner to fit its adjacent edges.
- **4 masters:** wght {Light 200, Black 900} × ROND {0, 100}. ROND = % of the maximum radius (half the local stem). Named instances: Thin…Black × Sharp/Round.

**Layout (each file ≤ ~300 lines):**
```
computer-font/
  README.md  CLAUDE.md  OFL.txt  LICENSE-CODE (MIT)  AUTHORS.txt  CHANGELOG.md
  .gitignore  requirements.txt  Makefile  pyproject.toml
  docs/superpowers/specs/2026-11-26-computer-font-design.md   # this design
  scripts/fetch_reference.sh          # downloads original → reference/ (gitignored)
  src/computerfont/
    config.py        # family name, UPM 1000, cap/x-height, ascender/descender, axis ranges, master params
    geometry.py      # Pt, Polygon, orthogonal path builder helpers
    corners.py       # compatible corner rounding (degenerate at r=0)
    components.py    # reusable parts: stem, bar, bowl, notch, dot, tail, comma — DRY core
    registry.py      # @glyph("A", 0x41, width=...) decorator + lookup
    glyphs/ uppercase.py  lowercase.py  digits.py  punctuation.py  symbols.py
    ufo.py           # draw registry → ufoLib2 Font per master (metrics, names, OS/2)
    designspace.py   # 2 axes, 4 masters, named instances
    build.py         # CLI: generate UFOs → fontmake variable TTF + woff2 + static instances
    proof.py         # PNG/HTML specimen across the axis grid
  tests/ test_geometry.py  test_corners.py  test_compat.py  test_charset.py
  specimen/index.html # browser test page with wght/ROND sliders (loads build woff2)
  .github/workflows/build.yml  # test + build on push; attach fonts to release on tag
  build/ fonts/ sources/generated/ reference/   # all gitignored outputs
```
**Rule of three:** any shape used in 3+ glyphs (stem, crossbar, notch, terminal, dot) lives in `components.py`. Glyph files only compose those parts.

## Execution — agents & todo list
I orchestrate, review each result, and commit. Agents don't commit, which avoids collisions in the shared working tree.

| Phase | Agent (model) | Tasks |
|---|---|---|
| A (parallel) | **Haiku-1** | README, CLAUDE.md (conventions, DRY/file-size rules, build commands, interpolation constraint), .gitignore, OFL.txt, LICENSE-CODE, AUTHORS, CHANGELOG, requirements.txt, pyproject, Makefile, fetch_reference.sh |
| A | **me** | write the design spec doc; `git init`; commit; `gh repo create areimel/computer-font --public --source . --push` |
| B | **Sonnet-1** | engine: config, geometry, corners, components, registry, ufo, designspace, build CLI, tests; proves the pipeline with ~5 sample glyphs (H O n o period) |
| C (parallel) | **Sonnet-2** uppercase A–Z · **Sonnet-3** lowercase a–z · **Sonnet-4** digits + punctuation · **Sonnet-5** symbols (# $ % & @ brackets, etc.) · **Haiku-2** proof.py + specimen/index.html · **Haiku-3** GitHub Actions CI | each works only in its own file(s); new shared parts go into components.py through me |
| D | **Sonnet-6** spacing/sidebearings + basic kerning, visual QA vs reference · **Sonnet-7** DRY/code review (file sizes, duplication) · **Haiku-4** final README with specimen image, CHANGELOG v0.1.0 | |

**Commit checkpoints (~10):**
1. scaffold & docs + design spec
2. push public repo
3. geometry + corner engine + tests
4. UFO/designspace/build pipeline + sample glyphs
5. uppercase
6. lowercase
7. digits & punctuation
8. symbols
9. proof/specimen page
10. CI
11. spacing/kerning
12. review cleanup
13. README/v0.1.0. Push after each.

## Verification
- `make test`: pytest covers geometry, the corner math (r=0 handles degenerate), **master compatibility** (identical point structure in all 4 masters for every glyph), and the charset (exactly U+0020–007E + .notdef; nothing outside it).
- `make build`: fontmake builds `ComputerFont[wght,ROND].ttf` + woff2 with no errors. A fontTools check confirms the `fvar` axes and ranges.
- `make proof`: render a wght × ROND grid PNG. I read the image to eyeball it against the reference charmap.
- Open `specimen/index.html` in the browser (Playwright) and move the sliders to confirm live variation.
- CI is green on GitHub; `gh repo view areimel/computer-font` shows a public repo with README.
