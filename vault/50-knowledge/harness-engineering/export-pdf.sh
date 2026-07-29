#!/usr/bin/env bash
# Batch-export lessons/ and reference/ to PDF for offline reading (ReMarkable).
# Run periodically: ./export-pdf.sh
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/pdf"

if [ ! -x "$CHROME" ]; then
  echo "Google Chrome not found at: $CHROME" >&2
  exit 1
fi

mkdir -p "$OUT/lessons" "$OUT/reference"

export_one() {
  local src="$1" dest="$2"
  echo "  $(basename "$src") -> ${dest#"$ROOT"/}"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$dest" \
    "file://$src" >/dev/null 2>&1
}

echo "Exporting lessons..."
shopt -s nullglob
for f in "$ROOT"/lessons/*.html; do
  export_one "$f" "$OUT/lessons/$(basename "${f%.html}").pdf"
done

echo "Exporting reference docs..."
for f in "$ROOT"/reference/*.html; do
  export_one "$f" "$OUT/reference/$(basename "${f%.html}").pdf"
done

echo "Done. PDFs in $OUT — copy that folder to your ReMarkable."
