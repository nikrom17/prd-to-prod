---
name: prd-vet
description: Stage 1 of prd-to-prod. Turns intake inputs (idea chat, rough PRD, design canvas flows.md) into one vetted, versioned prd.md with a Decisions section, option-research briefs, and consistency checks, up to the PRD-approved gate. Use after intake, or when Nik asks to sync or revise a PRD.
---

# Stage 1 · PRD shaping and vetting

Output: `prd.md` (one current version, older ones in `archive/`), `research/options-<topic>.md` briefs, and an updated `STATUS.md`. These are defaults, not a script (decision 31): skip what the inputs already answer, and don't research what Nik already decided.

## 1. Reconcile the inputs (first pass on any existing material)

Read every input listed in `intake.md` in full. With a design canvas, read `flows.md` and `elements.json` at the version intake recorded (or the latest, and record it).

- **Newest intent wins as the draft, never silently.** Put each conflict between inputs into the Decisions section: what each source says (cite `inputs/…` § or a screen number), options, and a recommendation (usually the newer source). Nik confirms each one.
- **Flows marked Final** become requirements. **In-progress flows** go in as provisional: requirement text tagged `(provisional: flow N in progress)`.
- **Design decisions** (D-xx in `flows.md`) stay in `flows.md`. The PRD links to them and lists only the ones that change product behavior. Don't copy the visual rules.
- **Open design decisions that block a requirement** get a PRD decision that points at the `flows.md` one (`see flows D-12`), so Nik answers in one place.

## 2. Draft with the standard outline

| Part | Contents |
|---|---|
| Header | Status, version, owner, sources with versions (chat, canvas version, earlier PRD), next steps |
| §1–4 | Overview, goals, non-goals (including content rules), users and context |
| §5 | Views and flows: a table of views, then the flow list with screen ranges, the link to `flows.md`, the fidelity level, and the design-versions table (gate, canvas version, date) |
| §6 | Functional requirements, one subsection per capability. Each requirement has an ID (`R-6.2.1`) and cites the flows and edge cases it comes from (`2.6, EC-2.6-1`). |
| §7 | Data and state: each kind of data, its owner and location, and how it resets |
| §8–9 | Design (link to the canvas and `elements.json`, plus the few product-level design rules), success |
| §10–11 | Risks (every Unverified claim lives here, with a fallback), and what must be validated before use |
| §12–13 | References (each source → the sections it feeds), Decisions (section 6.0 format). With a design canvas, PRD decisions are numbered **P-xx** so they never clash with the canvas's D-xx. Questions that aren't decisions go in a short Q-xx table. |

Label every Open decision **Decision** (Nik's preference settles it), **Explore** (only evidence settles it, so it goes to stage 2), or **Default** (the skill picks the simplest option and logs it). Tag every external claim **Verified** (with a source) or **Unverified**.

## 3. Option research (automatic)

Start a brief when a requirement names an outcome but not a mechanism, when Nik says "I don't know" or "whatever's best", when it touches auth, payments, notifications, an outside integration, storage or sync, AI, or device and OS behavior, or when the default stack doesn't cover it. A research subagent writes `research/options-<topic>.md`: 2–4 options (how each works, setup, cost, how it fails, fit with the default stack), every claim Verified or Unverified, a recommendation, and what each option needs proven (POC candidates). Nik picks with one question per topic: an option now, send it to stage 2, or "you decide".

## 4. Questions

Ask only what the inputs don't answer, in batches of 12 or fewer, multiple-choice where possible. The 11 categories, for coverage: users and context, views and navigation, core objects, live behavior and state machines, notifications, content and rules, data and state, reuse, design, scope and success, security and exposure. Flag the top 5 gaps that would change the architecture. Echo back an "I read your answers as…" table before the next draft.

## 5. Consistency checks (before showing each version)

Traceability (goal ↔ requirement ↔ view/flow), non-goals vs requirements line by line, content rules, state ownership and reset (including a cache clear), offline behavior per action (works offline? queued? ordering and idempotency on reconnect?), a walkthrough of the primary flow with edge timings, platform states (Home Screen app vs tab; foreground, background, killed), exposure (public vs private routes and APIs), and terms and numbers matching across sections. With a canvas: every flow and edge case maps to a requirement or is listed as design-only.

## 6. Revisions and the gate

After the first full draft, show deltas only, by section. Log each version in the header (trigger, changes, new decisions). When Nik pushes back, fix the rule and re-check similar items. Keep one current `prd.md`; earlier versions go to `archive/`.

**PRD-approved** means: every decision is Decided or deferred with an owner; every check passed on the final version; with a UI, design-sync ran on the pinned canvas version with no Open discrepancies and Nik approved stage 1b; a data plan exists; and Nik said "approved" in words. Explore items don't block this gate.
