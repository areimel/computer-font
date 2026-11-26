#!/usr/bin/env bash
# Downloads the original 1992 "Computerfont" for visual reference only.
# The output goes to reference/, which is gitignored and must never be committed.
set -euo pipefail

URL="https://dl.dafont.com/dl/?f=computerfont"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/reference"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$OUT_DIR"

curl -fsSL -o "$TMP_DIR/computerfont.zip" "$URL"
# Extract only the TTF, flattened into reference/ (no archive paths are kept).
unzip -o -j "$TMP_DIR/computerfont.zip" 'Computerfont.ttf' -d "$OUT_DIR"

echo "Saved $OUT_DIR/Computerfont.ttf"
echo "Note: this file is for visual reference only. Do not commit or redistribute it."
