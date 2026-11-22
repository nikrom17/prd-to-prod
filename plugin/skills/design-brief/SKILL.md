---
name: design-brief
description: The fixed, versioned prompt Nik pastes into a Claude Design chat so the canvas follows the prd-to-prod conventions (flows.md, elements.json, tokens, screen frames). Use when Nik asks for the design prompt, starts or resumes a Claude Design chat, or a design-sync finding says the canvas is on an older brief version.
---

# design-brief

The only source for what the design chat is told. Never write design-chat instructions on the fly. If a convention needs to change, edit `brief.md` or `elements.schema.json`, bump the version in both places, and tell Nik to paste the new brief again.

## Run

1. Run `sh "${CLAUDE_SKILL_DIR:-$(dirname "$0")}/copy-brief.sh"`. It joins `brief.md` with `elements.schema.json` and copies the result to the clipboard. Use `--print` to show it instead.
2. For a canvas that existed before the brief: after Nik pastes the brief and the design agent lists the gaps, run `copy-brief.sh adopt "<current pages>"` for the follow-up prompt (`adopt.md`). Ask Nik which pages are current first, because everything else gets archived.
3. Tell Nik the version (the first line) and that it's ready to paste into the Claude Design chat. Don't repeat the brief in chat.

## Files

| File | Role |
|---|---|
| `brief.md` | The prompt. Rules R1–R13. `{{ELEMENTS_SCHEMA}}` is replaced when copying. |
| `elements.schema.json` | Strict schema for the canvas's `elements.json` (decision 27). The design-sync validator validates against this same file. |
| `adopt.md` | Fixed follow-up prompt: bring an existing canvas in line (restructure only, no visual changes). |
| `copy-brief.sh` | Assembles and copies; `adopt` copies the follow-up. |

## Versioning

- The version string `design-brief vN` appears in: the `brief.md` title, `elements.schema.json` (`brief` const and `$id`), and the `flows.md` header the design chat writes (R1).
- design-sync reads the canvas's `brief:` value. If it's older than this file, that's a decision for Nik (re-paste, or accept the older conventions for this gate), not an automatic failure.
- design-sync cites rule numbers (R1–R13) in its findings, so keep the numbers stable: add new rules at the end, and mark removed ones "retired" instead of renumbering.
