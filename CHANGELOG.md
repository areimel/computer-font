# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-26

### Added

- Parametric engine: glyphs are orthogonal polygons drawn in Python from shared metrics, with compatible corner rounding and UFO masters per location.
- Variable font with `wght` (200 to 900) and `ROND` (0 to 100) axes, compiled to TTF and WOFF2, with named instances from ExtraLight to Black in Sharp and Round styles.
- Full printable ASCII character set (U+0020 to U+007E, 95 glyphs plus `.notdef`).
- Proof and specimen tooling: wght x ROND grid and size waterfall PNGs, a README banner, a fast per-master glyph preview script, and a browser specimen page with live sliders.
- Continuous integration: tests and build on every push and pull request, and fonts attached to a GitHub Release when a `v*` tag is pushed.
