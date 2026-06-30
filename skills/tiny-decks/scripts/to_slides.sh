#!/usr/bin/env bash
#
# to_slides.sh — upload a .pptx to Google Drive, converting to native Google
# Slides, and print the shareable link.
#
# Usage:
#   bash to_slides.sh <file.pptx> ["Optional Deck Title"]
#
# Requires: gog (the configured Google CLI) and jq.
# gog uploads with --convert-to slides and emits JSON containing the new file's
# id and webViewLink; we parse that and print the link. If a title is given it
# is passed as the Drive file name.
#
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage: bash to_slides.sh <file.pptx> ["Optional Deck Title"]

  <file.pptx>       Path to the PowerPoint file to upload.
  "Deck Title"      Optional. Names the resulting Google Slides file.

Uploads to Google Drive as native Google Slides via:
  gog drive upload "<file>" --convert-to slides -j
and prints the shareable link.
EOF
  exit 2
}

# --- args ---------------------------------------------------------------------
[ "$#" -ge 1 ] || usage
PPTX="$1"
TITLE="${2:-}"

# --- preflight ----------------------------------------------------------------
if [ ! -f "$PPTX" ]; then
  echo "error: file not found: $PPTX" >&2
  exit 1
fi

if ! command -v gog >/dev/null 2>&1; then
  echo "error: 'gog' CLI not found on PATH. Install/configure the Google CLI." >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: 'jq' not found on PATH. Install jq to parse the upload response." >&2
  exit 1
fi

# --- build the upload command -------------------------------------------------
# Base: upload + convert to native Slides + JSON output.
# If a title was supplied, pass it as the Drive file name (gog --name).
set -- drive upload "$PPTX" --convert-to slides -j
if [ -n "$TITLE" ]; then
  set -- "$@" --name "$TITLE"
fi

# --- run ----------------------------------------------------------------------
# Capture stdout (JSON) separately so a gog failure gives a clear message.
if ! RESPONSE="$(gog "$@" 2>/tmp/to_slides.err)"; then
  echo "error: gog upload failed:" >&2
  cat /tmp/to_slides.err >&2 || true
  exit 1
fi

# --- parse the link -----------------------------------------------------------
# Prefer webViewLink; fall back to constructing one from the file id.
LINK="$(printf '%s' "$RESPONSE" | jq -r '
  .webViewLink
  // .file.webViewLink
  // (if (.id // .file.id) then "https://docs.google.com/presentation/d/\(.id // .file.id)/edit" else empty end)
  // empty
')"

if [ -z "$LINK" ] || [ "$LINK" = "null" ]; then
  echo "error: could not find a link in the gog response:" >&2
  printf '%s\n' "$RESPONSE" >&2
  exit 1
fi

if [ -n "$TITLE" ]; then
  echo "✓ Uploaded \"$TITLE\" as Google Slides:"
else
  echo "✓ Uploaded as Google Slides:"
fi
echo "$LINK"
