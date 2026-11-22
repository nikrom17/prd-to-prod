#!/bin/sh
# Assemble the design brief (brief.md + elements.schema.json) and copy it to the clipboard.
# Usage: copy-brief.sh [adopt] [--print]
#   (no arg) the brief: brief.md + elements.schema.json
#   adopt "<current pages>"   the follow-up prompt that brings an existing canvas in line with the brief
set -eu
dir="$(cd "$(dirname "$0")" && pwd)"
if [ "${1:-}" = "adopt" ]; then
  shift
  pages="${1:?adopt needs the current page names, e.g. adopt \"the Final page\"}"; shift
  out="$(sed -n '/^---$/,$p' "$dir/adopt.md" | sed 1d | sed "s/{{CURRENT_PAGES}}/$pages/")"
else
out="$(python3 -I -c '
import sys, pathlib
d = pathlib.Path(sys.argv[1])
brief = (d / "brief.md").read_text()
schema = (d / "elements.schema.json").read_text().rstrip()
assert "{{ELEMENTS_SCHEMA}}" in brief
sys.stdout.write(brief.replace("{{ELEMENTS_SCHEMA}}", schema))
' "$dir")"
fi
if [ "${1:-}" = "--print" ]; then
  printf '%s\n' "$out"
else
  printf '%s\n' "$out" | pbcopy
  printf '%s\n' "$out" | head -1
  echo "Copied to clipboard ($(printf '%s' "$out" | wc -l | tr -d ' ') lines). Paste it into the Claude Design chat."
fi
