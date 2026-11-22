#!/bin/sh
# Assemble the design brief (brief.md + elements.schema.json) and copy it to the clipboard.
# Usage: copy-brief.sh [<prompt> ["<current pages>"]] [--print]
#   (no arg) the brief: brief.md + elements.schema.json
#   adopt "<current pages>"   bring an existing canvas in line with the brief
#   migrate-v2-propose        v1 canvas: propose the new screen numbers (send with the v2 brief)
#   migrate-v2-apply          v1 canvas: apply the approved numbers
set -eu
dir="$(cd "$(dirname "$0")" && pwd)"
if [ -n "${1:-}" ] && [ "$1" != "--print" ]; then
  name="$1"; shift
  [ -f "$dir/$name.md" ] || { echo "No prompt named $name (have: adopt, migrate-v2-propose, migrate-v2-apply)"; exit 1; }
  pages=""
  if [ -n "${1:-}" ] && [ "$1" != "--print" ]; then pages="$1"; shift; fi
  if grep -q "{{CURRENT_PAGES}}" "$dir/$name.md" && [ -z "$pages" ]; then echo "$name needs the current page names"; exit 1; fi
  out="$(sed -n '/^---$/,$p' "$dir/$name.md" | sed 1d | sed "s/{{CURRENT_PAGES}}/$pages/")"
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
