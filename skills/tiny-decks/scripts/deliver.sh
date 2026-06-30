#!/usr/bin/env bash
#
# deliver.sh — produce all three deliverables from one .pptx and (optionally)
# save copies to Google Drive.
#
#   1. PowerPoint  — the .pptx you pass in (already editable).
#   2. PDF         — board-ready, one slide per page (via LibreOffice).
#   3. Google Slides — native, editable (via the Drive connector / gog).
#   + saves the .pptx and .pdf into a Drive folder if --drive-folder is given.
#
# Usage:
#   bash deliver.sh <deck.pptx> ["Deck Title"] [--slides] [--pdf] \
#        [--drive-folder <FolderID|name>]
#
# The .pptx you pass in is the PowerPoint deliverable (always kept). Add:
#   --slides   also upload a native Google Slides copy (returns the link)
#   --pdf      also export a board-ready PDF
# The skill drives these from the user's choices: it asks "PowerPoint, Google
# Slides, or both?" then "Generate a PDF too?" and passes the matching flags.
#
# Requires: LibreOffice (soffice) for PDF; gog (Google CLI) + jq for Slides/Drive.
# Each requested step degrades gracefully — a missing tool prints a note and is
# skipped.
set -uo pipefail

usage() { echo "Usage: bash deliver.sh <deck.pptx> [\"Title\"] [--slides] [--pdf] [--drive-folder <id|name>]" >&2; exit 2; }

[ "$#" -ge 1 ] || usage
PPTX="$1"; shift
TITLE=""
DRIVE_FOLDER=""
WANT_SLIDES=0
WANT_PDF=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --slides) WANT_SLIDES=1; shift;;
    --pdf) WANT_PDF=1; shift;;
    --drive-folder) DRIVE_FOLDER="${2:-}"; shift 2;;
    *) TITLE="$1"; shift;;
  esac
done
[ -f "$PPTX" ] || { echo "error: file not found: $PPTX" >&2; exit 1; }

DIR="$(cd "$(dirname "$PPTX")" && pwd)"
BASE="$(basename "${PPTX%.*}")"
PDF="$DIR/$BASE.pdf"
[ -n "$TITLE" ] || TITLE="$BASE"

echo "▸ PowerPoint: $PPTX"

# --- PDF (LibreOffice) — only if requested -----------------------------------
if [ "$WANT_PDF" -eq 1 ]; then
  SOFFICE=""
  for c in soffice /Applications/LibreOffice.app/Contents/MacOS/soffice libreoffice; do
    command -v "$c" >/dev/null 2>&1 && { SOFFICE="$c"; break; }
    [ -x "$c" ] && { SOFFICE="$c"; break; }
  done
  if [ -n "$SOFFICE" ]; then
    "$SOFFICE" --headless --convert-to pdf "$PPTX" --outdir "$DIR" >/dev/null 2>&1 \
      && echo "▸ PDF:        $PDF" \
      || echo "  (PDF conversion failed)"
  else
    echo "  (LibreOffice not found — skipping PDF; in Cowork, ask Claude to export PDF)"
  fi
fi

# --- Google Slides + Drive save — only if requested --------------------------
if [ "$WANT_SLIDES" -eq 1 ]; then
  if command -v gog >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    FOLDER_ARG=()
    [ -n "$DRIVE_FOLDER" ] && FOLDER_ARG=(--parent "$DRIVE_FOLDER")
    RESP="$(gog drive upload "$PPTX" --convert-to slides --name "$TITLE" "${FOLDER_ARG[@]}" -j 2>/dev/null)"
    LINK="$(printf '%s' "$RESP" | jq -r '.webViewLink // .result.webViewLink // empty' 2>/dev/null)"
    if [ -n "$LINK" ]; then
      echo "▸ Slides:     $LINK"
    else
      echo "  (Slides upload returned no link; raw: $(printf '%s' "$RESP" | head -c 200))"
    fi
  else
    echo "  (gog/jq not found — skipping Google Slides; in Cowork use the Drive connector to upload + convert)"
  fi
fi

# --- save copies to a Drive folder, if requested -----------------------------
if [ -n "$DRIVE_FOLDER" ] && command -v gog >/dev/null 2>&1; then
  gog drive upload "$PPTX" --parent "$DRIVE_FOLDER" >/dev/null 2>&1 && echo "  saved .pptx to Drive folder"
  [ -f "$PDF" ] && gog drive upload "$PDF" --parent "$DRIVE_FOLDER" >/dev/null 2>&1 && echo "  saved .pdf to Drive folder"
fi

echo "✓ delivery complete"
