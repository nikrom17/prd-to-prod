#!/usr/bin/env python3
"""Mechanical design-sync checks on a canvas snapshot (design-brief v2).

Usage: check.py <canvas-project-dir> <schema.json> [<state.json>]

<canvas-project-dir> holds flows.md, elements.json, styles.css and the *.dc.html pages
(as saved by an Artifact read). <state.json> is the project's design-sync.json from the
last run (numbers and names ever seen, file hashes). Prints a JSON report to stdout.
Read-only: never writes anything.
"""
import hashlib, json, re, sys
from pathlib import Path

d = Path(sys.argv[1]); schema_path = Path(sys.argv[2])
state = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 and Path(sys.argv[3]).exists() else {}
findings = []  # {rule, severity: error|warn|info, msg}
def add(rule, sev, msg): findings.append({"rule": rule, "severity": sev, "msg": msg})

flows = (d / "flows.md").read_text()
m = re.search(r"^brief:\s*(.+)$", flows, re.M)
brief = m.group(1).strip() if m else None
if brief != "design-brief v2": add("R1", "error", f"flows.md header says {brief!r}, expected 'design-brief v2'")

body = flows.split("## Former IDs", 1)[0]
decisions_part = body.split("## Decisions", 1)
flows_part = decisions_part[0]

# Screens (R2, R14)
rows = re.findall(r"^\| (\d+\.\d+\.\d+) \| ([a-z][a-z0-9.-]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|", flows_part, re.M)
num2name, name2num = {}, {}
for n, nm, fid, data, step in rows:
    num2name.setdefault(n, set()).add(nm); name2num.setdefault(nm, set()).add(n)
for n, s in num2name.items():
    if len(s) > 1: add("R14", "error", f"screen {n} has several names: {sorted(s)}")
for nm, s in name2num.items():
    if len(s) > 1: add("R14", "error", f"name {nm} is on several numbers: {sorted(s)}")
for n, nm, fid, data, step in rows:
    if fid.strip() not in ("-", "Close", "Rough", "None"): add("R2", "error", f"{n}: fidelity {fid.strip()!r}")
    if not step.strip(): add("R2", "error", f"{n}: empty Step")

# Sub-flow headings and numbering
subflows = re.findall(r"^### (\d+\.\d+) · (.+)$", flows_part, re.M)
flows_h = re.findall(r"^## (\d+) · (.+)$", flows_part, re.M)

# Never reuse: a number or name seen before must keep its partner
seen = state.get("screens", {})  # number -> name
for n, s in num2name.items():
    nm = next(iter(s))
    if n in seen and seen[n] != nm:
        add("R14", "error", f"screen {n} was {seen[n]!r}, now {nm!r} (numbers are never reused)")
seen_names = {v: k for k, v in seen.items()}
for nm, s in name2num.items():
    n = next(iter(s))
    if nm in seen_names and seen_names[nm] != n:
        add("R14", "error", f"name {nm} was screen {seen_names[nm]}, now {n}")
gone = sorted(set(seen) - set(num2name))
retired = set(re.findall(r"^\| (\d+\.\d+\.\d+) \|[^\n]*Retired", flows_part, re.M))
for n in gone:
    if n not in retired: add("R14", "warn", f"screen {n} ({seen[n]}) disappeared without a Retired row")

# Edge cases (R3)
ecs = re.findall(r"^- (EC-(\d+\.\d+)-\d+):(.*)$", flows_part, re.M)
for ec, sf, text in ecs:
    for ref in re.findall(r"Screen: (\d+\.\d+\.\d+)", text):
        if ref not in num2name: add("R3", "error", f"{ec} points at missing screen {ref}")

# Status (R4)
status = re.findall(r"^\| ([^|]+?) \| (Final|In progress) \| ([0-9-]+) \|", flows, re.M)

# Decisions (R5)
decs = re.findall(r"^### (D-\d+) · (.+?)\s+Status: (Open|Decided)", flows, re.M)
nums = [int(x[0][2:]) for x in decs]
if len(nums) != len(set(nums)): add("R5", "error", "duplicate decision numbers")
for did, title, st in decs:
    blk = flows.split(f"### {did} ·", 1)[1].split("\n### ", 1)[0]
    if st == "Decided" and not re.search(r"^Outcome: \S", blk, re.M): add("R5", "warn", f"{did} is Decided with no Outcome")
prev_decs = state.get("decisions", {})
for did, title, st in decs:
    if did in prev_decs and prev_decs[did] != st: add("R5", "info", f"{did} {title}: {prev_decs[did]} -> {st}")
    if did not in prev_decs and prev_decs: add("R5", "info", f"new decision {did} {title} ({st})")

# Canvas pages: data-screen parity (R12)
pages = {p.name: p.read_text(errors="replace") for p in d.glob("*.dc.html")}
canvas_nums = {}
for name, html in pages.items():
    for n in re.findall(r'data-screen="(\d+\.\d+\.\d+)"', html): canvas_nums.setdefault(n, set()).add(name)
if canvas_nums:
    for n in sorted(set(num2name) - set(canvas_nums)): add("R2", "error", f"flows.md screen {n} isn't on the canvas")
    for n in sorted(set(canvas_nums) - set(num2name)): add("R2", "error", f"canvas screen {n} isn't in flows.md")
else:
    add("R12", "warn", "no data-screen attributes found (pages not in the snapshot?)")

# elements.json (R7-R8)
try:
    import jsonschema
    els = json.loads((d / "elements.json").read_text())
    errs = sorted(jsonschema.Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(els), key=str)
    for e in errs[:20]: add("R8", "error", f"elements.json: {e.message} at {list(e.path)}")
    ids = [e["id"] for e in els.get("elements", [])]
    if len(ids) != len(set(ids)): add("R7", "error", "duplicate element IDs")
    prev_ids = set(state.get("elements", []))
    for i in sorted(prev_ids - set(ids)): add("R7", "warn", f"element {i} disappeared (rename via replaced_by instead)")
    settled = [e["id"] for e in els.get("elements", []) if e.get("status") == "settled"]
except ImportError:
    add("R8", "warn", "jsonschema not installed; elements.json not validated"); ids, settled = [], []

# Hashes for change detection
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
hashes = {p.name: h(p) for p in sorted(d.iterdir()) if p.is_file()}
changed = sorted(k for k, v in hashes.items() if state.get("hashes", {}).get(k) not in (None, v))
added = sorted(k for k in hashes if k not in state.get("hashes", {})) if state else []

report = {
    "brief": brief,
    "counts": {"flows": len(flows_h), "subflows": len(subflows), "screens": len(num2name), "rows": len(rows),
               "edge_cases": len(ecs), "decisions": len(decs), "open_decisions": sum(1 for x in decs if x[2] == "Open"),
               "elements": len(ids), "settled_elements": len(settled)},
    "status": [{"scope": s.strip(), "state": st, "date": dt} for s, st, dt in status],
    "files_changed": changed, "files_added": added,
    "findings": findings,
    "new_state": {"screens": {n: next(iter(s)) for n, s in sorted(num2name.items())} | {k: v for k, v in seen.items() if k not in num2name},
                  "decisions": {did: st for did, _, st in decs}, "elements": sorted(set(ids) | set(state.get("elements", []))),
                  "hashes": hashes},
}
print(json.dumps(report, indent=1))
