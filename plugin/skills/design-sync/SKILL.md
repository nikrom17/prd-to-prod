---
name: design-sync
description: Validates a Claude Design canvas, then aligns the PRD to it. Screens mode (default, while Nik iterates) checks the design against itself and sends approved fixes to the design chat. PRD mode (once flows are Final) aligns the PRD to the screens. Run when Nik says the design changed, a flow is final, or sync. Never edits the canvas.
---

# design-sync

## Two modes

The cycle is design-led: rough PRD → first screens → design iterations where requirements get refined → validation of the screens → validation of the PRD, which mostly changes the PRD rather than the screens.

| Mode | When | Validator | Findings go to |
|---|---|---|---|
| **Screens** (default) | Nik says "design changed" or "sync" while iterating | `validator-screens.md`: the design against itself; the PRD isn't read | Fixes → the design chat as a change request, after Nik approves. Design choices → new open D-xx in `flows.md` (through the change request). |
| **PRD** | Flows are Final, before PRD-approved and HLD-ready, or when Nik asks to align the PRD | `validator-prd.md`: the PRD against the screens | PRD edits to match the screens (the screens win). P-xx only for what screens can't settle: data, sync, sign-in, security, imports. |

PRD decisions that change what's drawn are answered in the design chat during iteration. PRD mode records them afterward.

## Steps

1. **Read the canvas.** Use the Artifact tool (`action: read`) with `paths` for `project/flows.md`, `project/elements.json`, `project/styles.css`, and every current page (`project/*.dc.html` named in `inputs/design-canvas.md`). Note the version ID it returns.
2. **Mechanical checks.** Run `python3 check.py <saved project dir> <design-brief/elements.schema.json> <project>/design-sync.json`. It checks the brief version, numbering (R2, R3, R14, including never-reused numbers against the last run), decisions (R5), `data-screen` parity with the canvas (R12), and `elements.json` against the schema (R7–R8). It lists changed files and Status changes. It's read-only.
3. **Validator.** Start a fresh read-only subagent with the mode's prompt (`validator-screens.md` or `validator-prd.md`), filling in the paths. It never sees the lead's notes or opinions. If nothing in `flows.md` changed and check.py is clean, skip this step.
4. **Record findings** in the report, then:
   - **Screens mode:** show Nik the list, split into "fix now" (one-line fixes) and "log as open D-xx" (design choices). Send the ones he approves (step 6).
   - **PRD mode:** apply PRD edits that match the screens, and add P-xx only for what screens can't settle. Skip this while Nik has paused PRD changes; the findings wait in the report.
5. **Write the report** to `validation/design-sync/<date>-<version>.md`: version, counts, Status changes, check.py findings, validator findings, and what was recorded where. Update `design-sync.json` with check.py's `new_state` and the version. Add a line to `STATUS.md`. Commit.
6. **Change requests to the design chat.** For each approved design change (from a P-xx outcome or a design-only finding Nik accepts), write it as one line with its source in a changes file, then run `design-brief/copy-brief.sh change-request <changes file>`. Send it the way `design-brief/SKILL.md` describes, then re-run design-sync on the result.
7. **Pin at gates.** When Nik marks a version final at a gate, also save that version's current-page files and hashes to `validation/design-pins/<version>/` (decision 25), and render the curated screenshots (decision 39).

## Rules

- Nik makes every call. The validator and check.py never resolve anything.
- Never edit the canvas directly. Changes go through the design chat.
- Cite screen numbers, edge cases, and rule numbers (R1–R14) in every finding.

## Token notes (to tune)

- An Artifact read puts small text files (`elements.json`, `styles.css`) inline in the lead's context, about 20 KB each run. Only read them when `flows.md` mentions an element or token change, or when check.py needs a full run (first run, gates).
- Skip the validator when the only changes are fixes from an approved change request. Spot-check them in `flows.md` instead.
