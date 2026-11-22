---
name: design-sync
description: Keeps a project's PRD and its Claude Design canvas in sync. Run when Nik says the design changed, a flow is final, or before PRD-approved and HLD-ready. Reads the canvas, runs mechanical checks (check.py) and an independent read-only validator, and records findings as decisions in the doc they concern. Never edits the canvas.
---

# design-sync

## When

- Nik says "design changed", "flow N is final", or "sync".
- Before PRD-approved and before HLD-ready (on the version Nik marks final, which is then pinned).

## Steps

1. **Read the canvas.** Use the Artifact tool (`action: read`) with `paths` for `project/flows.md`, `project/elements.json`, `project/styles.css`, and every current page (`project/*.dc.html` named in `inputs/design-canvas.md`). Note the version ID it returns.
2. **Mechanical checks.** Run `python3 check.py <saved project dir> <design-brief/elements.schema.json> <project>/design-sync.json`. It checks the brief version, numbering (R2, R3, R14, including never-reused numbers against the last run), decisions (R5), `data-screen` parity with the canvas (R12), and `elements.json` against the schema (R7–R8). It lists changed files and Status changes. It's read-only.
3. **Validator.** Start a fresh subagent with `validator.md` as its prompt, filling in the paths. It gets only Read, Grep, and Glob. It never sees the lead's notes or opinions. It compares the changed flows with `prd.md` and returns findings. If nothing in `flows.md` changed and check.py is clean, skip this step.
4. **Record findings**, each in the doc it concerns, never in a separate file:
   - **Product mismatches** (the PRD and the flows disagree about behavior): a P-xx decision in `prd.md`, with both sides and options.
   - **Design-only issues** (a broken rule, a missing edge case): queued as a change request (step 6). Nik decides whether to send it.
   - **PRD updates that need no decision** (a flow marked Final makes its requirements non-provisional; new screens or edge cases in a flow add citations): listed in the report. Apply them to `prd.md` only when Nik is taking PRD changes. If he has paused PRD changes, they wait in the report.
5. **Write the report** to `validation/design-sync/<date>-<version>.md`: version, counts, Status changes, check.py findings, validator findings, and what was recorded where. Update `design-sync.json` with check.py's `new_state` and the version. Add a line to `STATUS.md`. Commit.
6. **Change requests to the design chat.** For each approved design change (from a P-xx outcome or a design-only finding Nik accepts), write it as one line with its source in a changes file, then run `design-brief/copy-brief.sh change-request <changes file>`. Send it the way `design-brief/SKILL.md` describes, then re-run design-sync on the result.
7. **Pin at gates.** When Nik marks a version final at a gate, also save that version's current-page files and hashes to `validation/design-pins/<version>/` (decision 25), and render the curated screenshots (decision 39).

## Rules

- Nik makes every call. The validator and check.py never resolve anything.
- Never edit the canvas directly. Changes go through the design chat.
- Cite screen numbers, edge cases, and rule numbers (R1–R14) in every finding.
