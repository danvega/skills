#!/bin/bash
# Render every HTML draft to a 1920x1080 PNG next to it.
#
#   render.sh draft-a.html draft-b.html ...
#
# Sequential on purpose: about 3 seconds per draft. Running several Chromes at
# once with --user-data-dir writes the PNGs but Chrome then never exits
# (observed 2026-09-14), so the parallel version hung every time.
# Output: <name>.png beside each <name>.html. One line per render.
set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ $# -gt 0 ] || { echo "usage: render.sh <draft.html>..." >&2; exit 1; }

for html in "$@"; do
  abs=$(cd "$(dirname "$html")" && pwd)/$(basename "$html")
  out="${abs%.html}.png"
  if "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
      --force-device-scale-factor=1 --window-size=1920,1080 \
      --screenshot="$out" "file://$abs" >/dev/null 2>&1; then
    echo "rendered $out"
  else
    echo "FAILED $html"
  fi
done
