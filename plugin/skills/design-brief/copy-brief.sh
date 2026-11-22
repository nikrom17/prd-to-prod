#!/bin/sh
# Copy the design brief, or one of its fixed follow-up prompts, to the clipboard.
# Usage: copy-brief.sh [<prompt> [<arg>]] [--print]
#   (no prompt)                    the brief: brief.md + elements.schema.json
#   adopt "<current pages>"        bring an existing canvas in line with the brief
#   migrate-v2-propose             v1 canvas: propose the new screen numbers (send with the v2 brief)
#   migrate-v2-apply               v1 canvas: apply the approved numbers
#   change-request <changes file>  approved changes, one per line with its source
set -eu
dir="$(cd "$(dirname "$0")" && pwd)"
print=0; prompt=""; arg=""
for a in "$@"; do
  if [ "$a" = "--print" ]; then print=1
  elif [ -z "$prompt" ]; then prompt="$a"
  elif [ -z "$arg" ]; then arg="$a"; fi
done
out="$(python3 -I - "$dir" "$prompt" "$arg" <<'PY'
import sys, pathlib
d = pathlib.Path(sys.argv[1]); prompt, arg = sys.argv[2], sys.argv[3]
if not prompt:
    brief = (d / "brief.md").read_text()
    schema = (d / "elements.schema.json").read_text().rstrip()
    assert "{{ELEMENTS_SCHEMA}}" in brief
    sys.stdout.write(brief.replace("{{ELEMENTS_SCHEMA}}", schema)); sys.exit()
names = sorted(p.stem for p in d.glob("*.md") if p.stem not in ("brief", "SKILL"))
f = d / f"{prompt}.md"
if prompt not in names:
    sys.exit(f"No prompt named {prompt} (have: {', '.join(names)})")
text = f.read_text().split("\n---\n", 1)[1].lstrip("\n")
for key in ("CURRENT_PAGES", "CHANGES"):
    tag = "{{" + key + "}}"
    if tag in text:
        if not arg: sys.exit(f"{prompt} needs an argument for {tag}")
        val = pathlib.Path(arg).read_text().strip() if key == "CHANGES" else arg
        text = text.replace(tag, val)
sys.stdout.write(text)
PY
)"
if [ "$print" = 1 ]; then
  printf '%s\n' "$out"
else
  printf '%s\n' "$out" | pbcopy
  printf '%s\n' "$out" | head -1
  echo "Copied to clipboard ($(printf '%s' "$out" | wc -l | tr -d ' ') lines). Paste it into the Claude Design chat."
fi
