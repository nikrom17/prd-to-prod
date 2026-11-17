#!/bin/sh
# Assemble the design brief (brief.md + elements.schema.json) and copy it to the clipboard.
# Usage: copy-brief.sh [--print]
set -eu
dir="$(cd "$(dirname "$0")" && pwd)"
out="$(python3 -I -c '
import sys, pathlib
d = pathlib.Path(sys.argv[1])
brief = (d / "brief.md").read_text()
schema = (d / "elements.schema.json").read_text().rstrip()
assert "{{ELEMENTS_SCHEMA}}" in brief
sys.stdout.write(brief.replace("{{ELEMENTS_SCHEMA}}", schema))
' "$dir")"
if [ "${1:-}" = "--print" ]; then
  printf '%s\n' "$out"
else
  printf '%s\n' "$out" | pbcopy
  printf '%s\n' "$out" | head -1
  echo "Copied to clipboard ($(printf '%s' "$out" | wc -l | tr -d ' ') lines). Paste it into the Claude Design chat."
fi
