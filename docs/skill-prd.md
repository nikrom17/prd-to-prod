# PRD: Idea-to-App skill

**Status:** Draft v3 (2026-11-15), ready for Nik's review. v3 adds UI flows, the element system, and design validation (sections 6.0 and 6.1b).
**Owner:** Nik
**Working name:** `idea-to-app`
**Related** (in `~/Claude/Projects/Weekly Meal Plan Auto Scheduler/` until housekeeping): `prd-step-retrospective.md` (how the Dunraven PRD was made), `prd-to-app-process.md` (how Dunraven Manor was built), `poc-plan.md` (how the meal-plan POCs were run), `housekeeping-plan.md`

---

## 1. Overview

A Claude Code skill that takes Nik from an idea to a deployed, verified app. The input can be a chat, a Notion page, or a rough PRD, plus, optionally, UI flows and screens designed in Claude Design. The skill shapes it into a vetted PRD, finds and tests the technical unknowns with POCs, writes an HLD, then builds the app with frozen acceptance criteria and an independent verifier.

It packages two processes that worked:

- **Meal planner (July 2026):** a PRD that separated product decisions from technical unknowns, about 20 single-question POCs on a shared template, and an adversarial audit of the results.
- **Dunraven Manor (October 2026):** an HLD with traceable IDs, criteria frozen before any code, contracts-first parallel building, and a fresh verifier every round, all on the deployed commit.

## 2. Problem

- Building without a validation loop produces apps that run but don't meet the requirements.
- A build loop can get stuck on a plan that is technically infeasible because a limitation was never explored (an API, a device, a platform, model accuracy, cost, or auth). That costs far more than a POC that turns out to be unnecessary.
- Rough PRDs drift as they get more detailed: sections contradict each other, and stale versions linger (the meal planner ended up with two PRDs that disagreed on the data model).
- Each project re-learns things an earlier POC already proved, such as push to a locked iPhone, Supabase connection strings, or the Google OAuth token expiry in Testing mode.

## 3. Goals

1. **Rough input to a vetted PRD:** reformat it to a standard structure, ask the questions that matter, and check consistency on every revision.
2. **Explore everything that could make the plan infeasible before the HLD.** Go broad: generate every plausible POC and let Nik cut the list.
3. **Reuse earlier results:** a private POC registry in git, searched before any new POC is proposed.
4. **A default tech stack,** so exploration focuses on what the stack doesn't already cover.
5. **Build with proof:** the app is done when an independent verifier confirms every acceptance criterion on the deployed commit.
6. **Nik only where a human is needed:** approvals, preferences, accounts and credentials, and checks only possible on a real device.
7. **Resumable at every step:** after a context compaction, a usage limit, or a week away.
8. **The UI Nik designed is a requirement,** at the fidelity he chooses: flows, screens, edge cases, and the element system are checked like any other criterion.

## 4. Non-goals

- No pruning on Nik's behalf. The skill recommends; Nik decides which POCs to skip.
- Not a hosted product, and not for multiple users. It's for Nik's personal projects.
- No stack choices outside the default stack unless the PRD needs it, and then only with Nik's approval.
- No production actions without an explicit authorization list.

## 5. User and context

- **User:** Nik. Writes requirements through conversation, often follows along from a phone via Remote Control, reviews documents quickly, and answers numbered questions by number.
- **Where it runs:** Claude Code. Ideas that start in a claude.ai chat can point at the public skill repo, or the chat can be pasted into stage 0.
- **Constraint:** Claude usage limits, not calendar time. Every stage reports its cost and spends it only where it moves a requirement toward proven.

## 6. Pipeline

Each stage has an input, an output, and a gate. A gate marked **Nik** waits for Nik's approval.

| # | Stage | Output | Gate |
|---|---|---|---|
| 0 | Intake | Project folder, `STATUS.md`, raw inputs saved as they are | — |
| 1 | PRD shaping and vetting | `prd.md` (versioned), with risks and a Decisions section; `research/options-*.md` briefs; `flows.md` in the design canvas (if there's a UI) | Design-sync validator; **Nik:** resolves its discrepancies |
| 1b | UI building blocks (skipped at No UI) | Pattern layer and final element spec, proposed from the screens | **Nik:** approves, then approves the PRD ("PRD-approved") |
| 2 | Feasibility triage | `pocs/CANDIDATES.md`: every candidate POC, with registry matches | **Nik:** cuts the list |
| 3 | POC runs | One folder per POC, on the standard template; results promoted to the registry | **Nik:** only for gated POCs (accounts, devices) |
| 4 | POC audit and PRD update | `pocs/AUDIT.md`, a revised PRD, and a GO / NOT YET verdict | **Nik:** approves "HLD-ready" |
| 5 | HLD | `hld.md`, plus "least confident" and "sections to double-check" lists | **Nik:** approves the HLD |
| 6 | Build harness | Build prompt, `.claude/agents/*`, `CLAUDE.md`, authorization list | — |
| 7 | Acceptance criteria | `validation/acceptance.json` and `REVIEW.md` | **Nik:** approves, then the criteria freeze |
| 8 | Build in waves | Contracts first, then parallel lanes in worktrees | Cost checkpoint after the first lane |
| 9 | Verify and checkpoints | One verifier round per milestone; reports and screenshots | **Nik:** manual checks at each milestone exit |
| 10 | Launch and teardown | Clean repo, scheduled jobs stopped, registry updated, retro, README screenshots from the live app | — |

### 6.0 Decisions and comments (every document)

Every md file the skill writes (PRD, `flows.md`, `CANDIDATES.md`, HLD, `REVIEW.md`, and this PRD) ends with a **Decisions** section. Questions live in the doc they're about, so nothing is written twice.

```
### D-07 · Superset delete confirm wording        Status: Open
Source: design-sync validator (canvas v1794766802-f0e4 vs flows.md)
Canvas says: "…moves up". flows.md says: "…is renumbered".
Options: (a) canvas wins (b) text wins (c) new wording
Recommend: (a)
Nik:
Outcome:
```

- **Open questions** are the decisions with status Open. There's no separate list.
- **Decided entries stay** as the record, and ship with the PR.
- **Validator findings** go into the Decisions section of the doc they concern, not a separate file.
- **Comments anywhere:** Nik can write `> NIK: …` at any point in a doc. On its next pass the skill answers each one in place or turns it into a decision.

### 6.1 Stage 1: PRD shaping and vetting

Source: `prd-step-retrospective.md` (how the Dunraven PRD was made, with its lessons applied).

**Intake (stage 0, before any questions)**

- Save Nik's raw idea verbatim: goals, pains, the "north star."
- Ask once: "Is there existing code, a POC, design docs, data sources (Notion, Docs), or a platform you want to reuse?" Fetch and read all of it before drafting. In Dunraven, drafting v1 without the POC doc cost a full version.
- Record:
  - workflow rules: the approval gates, what counts as approval, and where files may be written
  - hard context: deadline, environment (connectivity, devices), and content rules (spoilers, privacy, brand)

**Question framework**

- Ask questions in 11 categories, each with a default leaning:
  1. users and context
  2. views and navigation
  3. core objects
  4. live behavior and state machines
  5. notifications and alerts
  6. content and rules
  7. data and state
  8. reuse (one-off or generic)
  9. design
  10. scope and success
  11. security and exposure
- Flag the top 5 gaps that would change the architecture.
- Ask in batches of about 12 or fewer, multiple-choice where possible (AskUserQuestion). Thirty-six numbered questions in one message caused answer drift.
- **Echo back** an "I read your answers as…" table, and resolve any mismatch before drafting.

**Option research (automatic; Nik never has to say "explore this")**

Nik often knows the outcome but not the options. For example: "Log in with Face ID, plus a backup." Asking him to choose doesn't work when he doesn't know what the choices are. So the skill finds the choices itself.

- **Triggers.** Any one of these starts an options brief:
  1. A requirement names an outcome but not a mechanism ("Face ID login", "notify me", "sync with my calendar").
  2. Nik says "I don't know", "something like", or "whatever's best".
  3. The requirement touches a high-risk area: auth, payments, notifications, an outside integration, storage or sync, AI, or device or OS behavior.
  4. The default stack (section 8) doesn't cover it.
- **The brief:** a research subagent does desk research (official docs, the POC registry, the stack's proven capabilities) and writes `research/options-<topic>.md`. It contains:
  - 2–4 options, each with how it works, the setup, what it costs, and how it fails
  - how each option fits the default stack
  - every claim tagged Verified (with a source) or Unverified
  - a recommendation
  - what each option would need proven, which becomes a POC candidate
- **Nik picks** with one multiple-choice question per topic:
  - pick an option now, accepting its unverified parts as risks
  - send the topic to stage 2 so a POC can decide
  - or "you decide," and the recommendation is logged as a Decided entry in the Decisions section
- **Example: Face ID with a backup.** Likely options include a passkey (WebAuthn, where Face ID is the device's own check), a magic email link, recovery codes, and a password fallback. There's also the choice of who provides it: the database's built-in auth vs. an auth library. The brief would mark unverified items, such as whether passkeys work inside an iOS Home Screen web app, and those become POC candidates.

There are two kinds of exploration, and they happen at different stages:

| | Option research (stage 1) | Feasibility POC (stage 2–3) |
|---|---|---|
| Question | What are the choices? | Does the chosen option actually work in our setup? |
| Method | Desk research: docs, registry, stack | Code, real devices, real accounts |
| Cost | Small | Larger |
| Output | Options brief and a decision | POC doc and a registry entry |

**Draft with the standard outline**

| Part | Contents |
|---|---|
| Header | Status, version, owner, next steps |
| §1–4 | Overview, goals, non-goals (including content rules), users and context |
| §5 | Views table: View / Audience / Chrome. With a UI: the link to `flows.md` and the canvas, the fidelity level, and the design-versions table (section 6.1b) |
| §6 | Functional requirements, one subsection per view or capability |
| §7 | Data and state: owner and location for each kind of data |
| §8–9 | Design, success |
| §10–11 | Risks (unverified items and fallbacks), validate before use |
| §12–13 | References (each source → the section it feeds), Decisions (section 6.0: open and decided, with date, who, and why) |

For generic apps, add a "My configuration" section that keeps Nik's personal values apart from app behavior, as in the meal-plan PRD.

**Label every Open decision**

- **Decision:** Nik's preference settles it.
- **Explore:** only evidence settles it, so it goes to stage 2.
- **Default:** the skill picks the simplest option and logs it.

**Tag every external claim** as **Verified** (with a source) or **Unverified**. An unverified claim never appears as fact outside §10 Risks. Example: the cron-job.org free tier was stated as fact and never checked.

**Consistency checks, run before showing each version**

- **Traceability:** every goal maps to at least one requirement; every requirement maps to a goal and a view.
- **Non-goals:** re-read §3 against §6 line by line.
- **Content rules:** check every listed content item against each rule. The "Whodunnit" Act 3 mistake slipped through because this check was skipped.
- **State ownership:** each piece of state has exactly one owner and a reset behavior. Check what happens on a cache clear or storage eviction.
- **Offline:** for each action: does it work offline, what gets queued, and what ordering and idempotency apply on reconnect.
- **Flow walkthrough:** step through the primary flow end to end, including:
  - very short stages, and alerts that would land in the past
  - early advance, late advance, reset, and skip
  - bulk completion: which timers start, and which alerts get scheduled or cancelled
  - projection math
- **Platform states:** for example, an iOS browser tab vs. a Home Screen app; foreground, background, locked, killed.
- **Exposure:** shared URLs vs. private views and APIs on the same origin.
- **Terms and numbers:** times, durations, counts, and names match across sections.

In Dunraven, the HLD and the criteria review caught most of the PRD's gaps: auto-check scope, timer starts, projection math, short-stage alerts, stale retries, API exposure, and silent push. These checks move that work earlier, where it's cheaper. The HLD stays as a backstop.

**Revisions**

- After the first full draft, show deltas only, labeled by section.
- Log each version: the trigger, the changes, and any new decision-log entries.
- When Nik pushes back, fix the rule, not just the instance, and re-check every similar item.
- Keep exactly one current PRD. Earlier versions go to `archive/` with a pointer to the current one.

**PRD-approved** (the gate into stage 2) means:

- Every decision is Decided, or deferred with an owner.
- Every consistency check passed on the final version.
- With a UI: the design-sync validator ran on the pinned canvas version with no Open discrepancies, and Nik approved the stage 1b building blocks (section 6.1b).
- A data plan exists: either a frozen content inventory, or named references the HLD will derive content from.
- Nik approved explicitly, in words. Positive feedback alone isn't approval.

Explore items don't block this gate. They're what stage 2 is for. **HLD-ready** comes later, at stage 4, once every explore item is resolved by evidence or recorded as an accepted risk with a fallback.

### 6.1b UI flows, elements, and design validation (stages 1 and 1b)

Nik designs flows and screens in Claude Design. The PRD stays the "what and why"; `flows.md` is the written source of truth for UI behavior; the element spec says exactly what components to build.

**Fidelity levels.** Set per app in `idea-to-app.config.json` (`ui.fidelity`), with overrides per screen in `flows.md`.

| Level | What's checked | Stage 1b |
|---|---|---|
| **No UI** | Behavior only. Flows run end to end; the look uses stack defaults. A text-only `flows.md` is enough. | Skipped |
| **Rough mock** | The right elements and content on each screen, in the right order and layout regions. No geometry. | Patterns only |
| **Close** | Rough-mock checks, plus computed styles and element positions against the design (below). | Full |

**`flows.md`**

- Lives in the Claude Design canvas next to the screens. Nik has Claude Design update both. The repo holds only the canvas link and the pinned version, so there's one copy.
- Keeps the canvas's screen IDs (5k9, not a new numbering). Without a canvas, the skill writes `flows.md` from Nik's text.
- Format, per flow and sub-flow:

  ```
  ## F3 · Setup
  ### 3d · Delete a superset
  | Screen | Fidelity | Step |
  | 5k9  | Close | Trash in the header asks first. The confirm lists every exercise going with it. |
  | 5k12 | Close | After deleting A, letters follow position: B becomes A. Save turns on. |
  Edge cases:
  - EC-3d-1: the last superset in a workout can't be deleted (trash dimmed)
  ```

- The canvas's decision log ("what's locked for the HLD") and "Still open" list become `flows.md`'s Decisions section (6.0).
- Screens marked Mock or "depends on the HLD's findings" are flagged for option research and stage 2.

**Design versions**

- Each gate records the canvas version it approved in the PRD's design-versions table: gate, canvas version (for example `1794766802-f0e4`), date.
- **Tested 2026-11-15:** reading the canvas always returns the latest version, so an older version can't be read back later. Every read does return the version ID and a sha256 for each file. So when Nik marks a version final at a gate, the skill commits that version's files and hashes, read-only, to `validation/design-pins/<version>/` (D-25). Iterations in between are never saved.
- After a gate, Nik changes the design and sends a quick message ("updated the design: changed X"). The skill compares the current hashes against the pinned ones to find which files changed, diffs those against the saved pin, runs the validator on what changed, logs the discrepancies as decisions, and, after the freeze, adds criteria. Earlier criteria stay frozen.
- Design files are never kept as documentation. The gate pins exist only as validation evidence. README screenshots come from the live app at stage 10.

**Design-sync validator**

An independent, read-only agent, like the build verifier but for documents.

- **When:** before PRD-approved, before HLD-ready, and whenever Nik says the design changed.
- **Reads:** the canvas at the pinned version, `flows.md`, the PRD, and the element spec.
- **Checks:**
  - every canvas screen ID is in `flows.md`, and every `flows.md` screen is on the canvas
  - each caption matches its flow step, and each edge case on the canvas is in `flows.md`
  - the flows' decisions don't contradict the PRD (for example, the PRD says sign-up, the flows say "no sign-up")
  - screens use only elements in the spec
  - colors, type, and spacing are tokens, not raw values
- **Output:** entries in the Decisions section of the doc concerned, each showing both sides and options. Nik makes every call; the validator never resolves anything, and the skill doesn't move on while any are Open.

**Elements while iterating (the half step)**

Cheap habits that don't churn while flows are still changing. They're written down in the `design-brief` skill (decision 36), the fixed prompt Nik pastes into the Claude Design chat.

1. Each element gets a stable ID (`button.action`, `button.pair`) and a status: Draft or Settled. Only Settled elements get a full spec.
2. Spec data lives in `elements.json` in the canvas, and the Elements page is rendered from it. Build agents read the JSON.
3. No hand-written "used in". It's generated in stage 1b by scanning the screens.
4. Settled elements move from inline styles to classes in the canvas's `styles.css`, so changing an element in the design changes it on every screen. This is for editing the design; the app doesn't share that CSS.

**Stage 1b: UI building blocks**

- **When:** Nik says the flows are done. Before PRD-approved, so stage 2 sees the patterns.
- An agent reads every screen and proposes the pattern layer (for example: sheet with a sticky Cancel / Save bar, confirm sheet, exercise row, superset tile row, empty state), each listing the atoms it's made of and a generated "used in".
- Inconsistencies (two confirm sheets built differently) become decisions for Nik.
- After Nik approves, the final element spec is generated. Per element:

  ```yaml
  id: button.action            # level: atom | molecule | pattern
  status: settled
  base: shadcn Button + cva variants   # or "custom"
  variants: [accent, black, outlined]
  sizes: {action: 72, add: 52, control: 44}
  states: [default, pressed, dimmed, focus]
  tokens: [color-accent, color-text, font 600 14px]
  rules:
    - one accent per screen
    - accent on the right is what you came to do; black on the left is the way out
  a11y: real <button>, aria-label if icon-only
  composes: []
  used_in: [5y, 5k5, 5v2]      # generated
  ```

- Elements with no shadcn base (a number pad, tiles, steppers) need the most complete specs, since the builder starts from nothing.

**Matching design elements to app elements**

- **Type:** `data-slot`, `data-variant`, and `data-size`. shadcn components already emit `data-slot`; the base components add the other two once, so every use gets them. In the design, the attributes come from `elements.json`, so Nik never types them.
- **Instance:** role plus accessible name (button "Start workout"), the same way the end-to-end tests find elements.
- **Not chosen:** marker classes (styling classes get restyled; goes against shadcn's convention). One stylesheet shared by the design and the app would make drift nearly impossible, but it works against shadcn's styling model. It's a possible per-project POC, not the default.

**Close checks**

Playwright renders the design screen and the built screen at the same iPhone viewport and compares element by element, not pixel by pixel:

- **Computed styles** (color, font, padding, radius) must match the tokens exactly.
- **Boxes** (position, size) must fall within `ui.tolerance_px` in `idea-to-app.config.json`, starting at 2. Overlap, clipping, off-screen, or wrong order always fails.
- **Three-way triage** (spec, design screen, built app), so a design error isn't blamed on the build:

  | Design screen vs spec | App vs spec | Verdict |
  |---|---|---|
  | Matches | Off | Build bug: FAIL |
  | Off | Matches | The design is off: decision for Nik, not a build failure |
  | Off | Off, the same way | The spec may be outdated: decision |
  | Off | Off, differently | Both wrong: decision, and the build fails |

  The validator runs the design-vs-spec half before the build, so most "the design is off" cases are settled before code exists.
- **Rendering tested 2026-11-15:** Playwright (WebKit) rendered the canvas's sign-in screen locally from the canvas files served over local HTTP. It found both buttons by role and name, with boxes and computed styles. Measurements must be taken relative to the screen frame, not the artboard, because the artboard includes its caption (a 73px offset on 5y). The full comparison tool is still to be built with the skill.
- **That test caught a real design discrepancy:** the accent on the Final page is `oklch(0.62 0.21 35)`, overriding the token sheet's `#ec3013`, which the standalone SignIn component uses. The validator's token check exists for exactly this.

### 6.2 Stage 2: Feasibility triage (the explicit POC step)

**Rule:** go broad. A POC Nik cuts costs a minute of reading. A missed limitation can stall the build.

**The test for each requirement:** if this assumption is wrong, does the build *fail*, or does the app just *look different*? Fail means it's a candidate. Every requirement tagged Explore or Unverified in stage 1 starts on the list.

1. **Sweep the PRD for risk.** Check every requirement against these categories:
   - external APIs and integrations (access, quotas, deprecations, pricing)
   - auth and OAuth (token lifetimes, consent screens, Testing vs Production mode)
   - platform and device behavior (iOS PWA, push, background, watch)
   - LLM accuracy and cost
   - algorithmic difficulty (solvers, scheduling)
   - data availability and format
   - performance and scale
   - scheduling and cron
   - hosting limits
   - anything the default stack doesn't already prove
   - **UI flows:** walk `flows.md` screen by screen and edge case by edge case with the same fail-vs-look-different test. Interactions that work in the Claude Design prototype aren't proven in an installed iPhone web app (drag-up sheets, a custom number pad that keeps the iOS keyboard away, safe areas). These become **interaction POCs on a real iPhone**. Screens marked Mock or "depends on the HLD" start on the list.
2. **Check the registry** (section 7) for each candidate:
   - **Reuse:** a matching result is still fresh, so cite it and don't run a POC.
   - **Stale:** a match exists but is older than 6 months, or a major version or API changed since. The skill asks Nik in that session: re-certify it (a short re-run, which updates the registry entry) or use it as is (logged as an accepted risk).
   - **New:** no match.
3. **Check the stack's proven capabilities** (section 8). Anything already proven is listed as covered, not as a POC.
4. **Write `CANDIDATES.md`** for Nik's phone. It's the full list, never pre-filtered, grouped two ways:
   - **By importance:** tier 1 blocks the core feature, tier 2 blocks a secondary feature, tier 3 is de-risk only.
   - **By dependency:** POCs that can run in parallel are listed together in a wave. A POC that needs another POC's result goes in a later wave, with the dependency named ("needs P-03's schema").

   Each row has:
   - ID and the single question it answers
   - why it's risky, and what breaks for the user if the answer is no
   - the decision it feeds (or "de-risk only")
   - registry match and verdict
   - autonomy and session mode (from `poc-plan.md`): AUTO, AUTO-first-pass, or NIK-GATED; UNATTENDED, CHECK-IN, or PAIRED
   - an estimated cost
   - the skill's recommendation: run, reuse, or optional
5. **Nik reviews the full list and cuts it.** He replies by ID ("skip P-07, P-12"). Skipped items are logged as accepted risks and carried into the HLD's risk section. If a cut POC was a dependency of another, the skill says so before accepting the cut.
6. **Finalize the waves:** order the POCs so nothing downstream guesses at a format an upstream POC creates (the meal planner's building-block model). Each POC gets a self-contained `PROMPT.md`.

### 6.3 Stage 3: POC runs

- Every POC uses the standard doc template from `poc-plan.md`: goal and question, context, what was built, test inventory, approach variations, reproduction, measurements, failures, decision, integration notes, and open items for Nik.
- **Background agents run the POCs.** The skill starts each wave's POCs as background agents, each in its own worktree and writing only inside its own POC folder. A wave starts when every POC it depends on has finished.
- **Gated POCs** (an account, a credential, OAuth consent, a device) do all the desk work first, then stop and send Nik step-by-step instructions. Other POCs keep running meanwhile.
- After each wave, the skill sends a short summary: verdicts, anything that changes a later POC, and the cost so far.
- **Code before Claude:** pipeline POCs measure how far plain code gets before an LLM is involved.
- **Secrets:** env var names only; values never go in the tree or the registry.
- Finished POCs are promoted to the registry (section 7).

### 6.4 Stage 4: POC audit and PRD update

- An adversarial audit re-runs every POC's tests, cross-checks headline numbers against the committed output, and checks the results against the PRD.
- Results feed back into the PRD:
  - unknowns become decisions
  - infeasible requirements are changed or cut, with Nik's approval
- With a UI: if POC results changed any flow, Nik updates the design and the design-sync validator runs again on the new version.
- Verdict: **GO**, or **NOT YET** with a short fix list. "HLD-ready" means no open unknowns that block the core feature.

### 6.5 Stages 5 to 10: HLD through launch

These follow `prd-to-app-process.md` (Dunraven Manor), with these changes:

- The HLD cites POC results and registry entries for every risky design choice, and lists the risks Nik accepted.
- The skill generates the agent definitions and the build prompt from templates, filled with this project's lanes, IDs, and production resources.
- **With a UI, the HLD imports the design instead of inventing it:**

  | From the design | Becomes |
  |---|---|
  | Each flow and sub-flow | User stories (US-xx traced to `3d`, and so on) |
  | Each step | An end-to-end test that walks the flow as written |
  | Each edge case | Its own criterion and test; `coverage.md` fails if any edge case has none |
  | The element spec | One component per atom and molecule, props from variants and states; a dev-only `/elements` gallery (like Dunraven's `/gallery/<id>`) |
  | Decisions such as heights and "one accent per screen" | Tokens, token-checker rules, and rubric items |
  | Close screens | Close checks (section 6.1b); the `/elements` gallery is compared to the Elements page once, then screens get composition and position checks |
  | Screen states | The data model and the HLD's state tables |

- Builders still don't style; the UI agent owns styling, working from the element spec.
- **One fixture library** (D-29) seeds local dev, tests, and the `/gallery/<screen-id>` routes; every canvas screen ID names its fixture.
- **Verifier rounds:** escalate to Nik after 2 rounds without exit (D-30).
- **Lean subagent sessions.** Every subagent's starting context costs tokens on every turn, multiplied across lanes and rounds:
  - **Tools:** each agent definition lists only the tools its role needs. Builders and the UI agent get no MCP servers; only the lead and the verifier get Vercel and Supabase.
  - **MCP and plugins:** the project's settings turn off plugins and MCP servers the build doesn't use (for example Notion, browser, and computer-use), so they don't load in agent sessions.
  - **Instructions:** `omitClaudeMd` on agents (as in Dunraven); prompts point at file paths and IDs instead of pasting content; skills load templates only when needed.
  - **Measure, don't guess:** at the first-lane cost checkpoint, record each role's starting context and per-turn cost, and cut anything that doesn't change output quality.
- **Fixes for friction seen in Dunraven:**
  - worktrees go outside the repo, or are excluded from test, typecheck, and lint
  - lead-only env files that subagents can't overwrite
  - the verifier gets a write path for its report
  - screenshot output never goes to committed folders
  - every test ID has an owning lane
  - a round is split so a usage limit doesn't waste it
- **Stage 10 (teardown):** remove worktrees, stop scheduled jobs, remove unused env vars and aliases, update the registry with anything learned during the build, and write a short retro.

## 7. POC registry

A private GitHub repo, `nikrom17/poc-registry`, cloned to `~/Claude/poc-registry` and shared across projects.

```
poc-registry/
├── INDEX.md               # one row per POC: what it proved, how fresh it is, and the verdict
├── index.json             # the same data, machine-readable for matching
├── capabilities/          # what the default stack has proven, with links to the evidence
└── pocs/
    └── 2026-07-poc-17-pwa-push/
        ├── README.md      # the standard POC doc
        ├── src/ tests/ fixtures/ out/
        └── meta.json      # see below
```

- **`meta.json`** holds:
  - source project
  - date
  - capability tags (for example `push.ios-pwa`, `oauth.google`, `llm.extraction`)
  - stack and versions
  - status and verdict
  - evidence paths
  - freshness notes, for example "Fitbit Web API deprecated Sept 2026"
  - a reusable module path, if there is one
- **Matching:** stage 2 searches tags and text in `index.json`, then reads the matching READMEs.
- **Freshness:** a result is stale after 6 months, after a major version change, or when a deprecation is noted. For a stale match, the skill asks Nik in that session: re-certify it, or use it as is (logged as an accepted risk).
- **Seed:** the 21 meal-plan POCs, POC-17's push pipeline, the Dunraven push hardening (the FCM 410 and subscription lock work), and the Supabase and Vercel setup learnings. Secrets get scrubbed first: the meal-plan audit found live OAuth tokens in POC folders.
- **Writes:** only stage 3 (a promotion) and stage 10 (learnings from the build), each with a commit message naming the project.

## 8. Default tech stack

The stack Dunraven Manor shipped on. Each part is marked with what it's proven to do, so stage 2 can skip those items.

| Layer | Choice | Proven by |
|---|---|---|
| Framework | Next.js 16.2 (App Router), React 19.2, TypeScript | Dunraven |
| Styling | Tailwind CSS v4 and shadcn/ui (Radix), every style value a token, enforced by a token checker. Base components carry `data-slot`, `data-variant`, `data-size` (section 6.1b). | Dunraven (shadcn Drawer for bottom sheets: not yet proven on iOS) |
| Validation | zod 4 | Dunraven |
| Database | Supabase Postgres with RLS on; Prisma 7.8 with the pg adapter; migrations through Prisma | Dunraven |
| Hosting | Vercel; pushing `main` deploys production | Dunraven, meal-plan |
| Scheduling | Supabase `pg_cron` and `pg_net` calling a bearer-protected route | Dunraven |
| Push and PWA | `web-push`, VAPID, a service worker; installable on iOS, push to a locked iPhone | POC-17, Dunraven |
| Tests | Vitest (unit and integration against local `prisma dev`), Playwright (WebKit iPhone and Chromium push), axe | Dunraven |
| LLM calls | A structured-output harness (schema in, validated object out, one repair pass) | Meal-plan A6 |
| Tooling | Claude Code with the Vercel and Supabase MCPs, `gh`, and Node 22 | Both |

Anything the PRD needs that this table doesn't cover (login, payments, maps, and so on) goes through option research in stage 1. The skill recommends an option and the POCs to prove it, and Nik picks. A proven result goes into the registry's `capabilities/`, so the next project can reuse it. It joins the scaffold template only if it's needed by nearly every project; most won't be.

## 9. Human touchpoints

| When | What Nik does | Format |
|---|---|---|
| Stage 1 | Answers interview questions; picks an option per research topic; resolves design-sync discrepancies | Multiple-choice batches of about 12 or fewer, each with a proposed answer; an echo-back table; `Nik:` lines in the Decisions section |
| Stage 1b | Approves the UI building blocks and element spec; approves the PRD | Proposal plus decisions |
| Any time after a gate | Sends a quick message when the design changed | One line; the skill does the rest |
| Stage 2 | Cuts the POC list; re-certifies or accepts stale registry matches | Reply by ID |
| Stage 3 | Accounts, OAuth consent, device steps (gated POCs only) | Step-by-step instructions with links |
| Stage 4 | Approves "HLD-ready" | Audit summary |
| Stage 5 | Approves the HLD after the "least confident" review | Numbered concerns |
| Stage 7 | Approves the criteria | `REVIEW.md` |
| Stage 8 | Picks a model after the cost checkpoint | Tokens and estimated cost |
| Stage 9 | Runs manual device checks; approves the UI | Report and screenshots |

Everything is readable on a phone: short messages, files sent rather than pasted.

## 10. Success metrics

- No build stalls because of a technical limitation that wasn't explored.
- Every PRD requirement traces to a criterion, and every criterion to evidence.
- With a UI: every screen ID and edge case in `flows.md` traces to a criterion.
- Each new project reuses at least one registry result, once the registry has a match.
- Verifier rounds to milestone exit stay at or below Dunraven's 4.
- Nik's time goes only to the touchpoints in section 9.

## 11. Decisions

Uses the format in section 6.0. Open items come first.

### D-28 · Build order for the skill        Status: Decided
Source: "least confident" review, 2026-11-15. The PRD describes about 8 skills, 2 validator agents, templates, a working scaffold app, a seeded registry, and a design comparison tool, none of it run end to end yet. Dunraven worked because each step was used right after it was written.
Options:
(a) Build just ahead of the Workout Log app: stages 0–1b plus design-sync first, used on Workout Log right away; then stages 2–4 when its PRD is approved; then the build loop (6–9) when its HLD is ready. The registry starts with only what Workout Log's POCs need, and the other meal-plan POCs are seeded later.
(b) Build the whole plugin first, run the sanity check, then start Workout Log.
Recommend: (a). Each stage gets a real run before the next one is written, and fixes land while the context is fresh.
Nik: sure. Build each part out and iterate using the workout app.
Outcome: (a), 2026-11-15.

### D-29 · How the built app shows each design screen        Status: Decided
Source: "least confident" review. Close checks compare design screen 5k9 to the same state in the built app. Most screen IDs are mid-flow states (a confirm sheet open, a workout half logged), so the app has to be able to show each one on demand.
Options:
(a) A dev-only state gallery like Dunraven's `/gallery/<id>`, one route per canvas screen ID, each rendering that state from fixture data. The HLD lists the fixture for every screen ID; the criteria check one screenshot per route.
(b) Playwright drives each flow to the state by tapping through it. No gallery code, but slower, flakier, and a broken step early in a flow hides every screen after it.
Recommend: (a) for Close and Rough screens; (b) is still used for the end-to-end flow tests, which check behavior.
Nik: yes, this goes into the dev/test data question. Can we combine that step with this step?
Outcome: (a), combined with test data, 2026-11-15. One fixture library per project, defined in the HLD: each fixture is a named data state (for example "workout half logged, A1 edited"). The same fixtures seed local dev, integration tests, end-to-end tests, and the `/gallery/<screen-id>` routes. Every canvas screen ID names its fixture, so the gallery, the tests, and the design all describe the same states.

### D-30 · Cost check before committing to Close fidelity        Status: Decided
Source: "least confident" review. Dunraven had 248 criteria and a handful of screens. Workout Log has about 70 screen IDs and dozens of edge cases at Close fidelity, so expect several hundred criteria and much heavier verifier rounds.
Options:
(a) After stage 7 (criteria), the skill estimates the cost of one verifier round, and Nik confirms Close for every screen or drops some to Rough.
(b) No check; Close everywhere.
Recommend: (a).
Nik: I'm okay with increased cost due to it being a more complex app. We can refine the validation loop as we go to make it as token efficient as possible. Maybe we stop at just 1 or 2 rounds.
Outcome: (b), 2026-11-15: Close everywhere, cost accepted. Changes to the loop: escalate to Nik after 2 verifier rounds without exit (Dunraven allowed 5), and tune token efficiency during the Workout Log build (for example, re-checking only failed criteria and criteria touched by changed files in round 2, while the integrity diff and mutations still run in full).

### D-25 · Where gate pins of the design are saved        Status: Decided
Source: version test, 2026-11-15 (section 6.1b, Design versions). The canvas can't return an older version, so each gate must save its own copy to diff against later.
Options:
(a) Commit to `validation/design-pins/<version>/`, read-only. It's evidence like the frozen criteria, never edited, and never read as documentation.
(b) Copy the version server side into a private "pin" artifact per gate. Nothing lands in the repo, but it adds one artifact per gate to your gallery, and it's untested.
(c) Save only the version ID and file hashes. No copies, but the validator can then say *which* files changed, not *what* changed.
Recommend: (a). It's small (about 2 MB for Workout Log without the type's own files), and the drift risk is low because nothing reads it except the validator.
Nik: a, yes, but only when it's marked as final. We don't need every iteration saved.
Outcome: (a), 2026-11-15. A pin is saved only when Nik marks a design version final at a gate (PRD-approved, HLD-ready, or a post-gate change he approves). Iterations in between are never saved.

**Decided 2026-11-15:**

1. **Packaging:** one master skill runs the stages in order. Each stage is also a sub-skill Nik can run alone, and it continues from that point using `STATUS.md`.
2. **Registry:** private GitHub repo `nikrom17/poc-registry`, cloned to `~/Claude/poc-registry`.
3. **Freshness:** stale after 6 months or a major change. The skill asks Nik in that session whether to re-certify it or use it as is (stage 2, step 2).
4. **Project layout:** one git repo per project from day one, created from the scaffold (section 12).
5. **Calibration:** a quick check against both Dunraven and the meal planner (section 13; narrowed by item 10).
6. **PRD template:** filled in from `prd-step-retrospective.md` (section 6.1).
7. **Unknown options:** stage 1 runs option research automatically (section 6.1). Nik picks an option, sends the topic to a POC, or lets the skill decide.

8. **Skills:** installed once from the scaffold repo as a plugin, not copied into each project (section 12).
9. **Public vs. private:** scaffold and skills public, POC registry private (section 12).

10. **Testing:** a quick sanity check, not an eval suite (section 13). The new app is the real shakedown; Nik adjusts the skill while building it.
11. **Features the stack doesn't cover** (like login): option research recommends an option and the POCs to prove it. Proven results go to the registry, not necessarily to the scaffold (section 8).
12. **Running POCs:** background agents, after Nik reviews the full list grouped by importance and dependency waves (sections 6.2 and 6.3).
13. **Where stage 1 runs:** Claude Code. claude.ai chats can reference the skill repo or be pasted in (section 5).
14. **Decisions in each doc:** every md ends with a Decisions section with `Nik:` lines; `> NIK:` comments work anywhere; validator findings go to the doc concerned (section 6.0).
15. **`flows.md`** lives in the Claude Design canvas, keeps the canvas's screen IDs, and sets fidelity per screen (section 6.1b).
16. **Design-sync validator:** independent and read-only; runs at each gate and on design changes; Nik decides every discrepancy (section 6.1b).
17. **Fidelity levels:** No UI, Rough mock, Close; per app with per-screen overrides (section 6.1b).
18. **Tolerance:** `ui.tolerance_px`, starting at 2; three-way triage separates design errors from build bugs (section 6.1b).
19. **Matching:** `data-slot` / `data-variant` / `data-size` following shadcn, plus role and accessible name (section 6.1b).
20. **Elements while iterating:** stable IDs, Draft / Settled, `elements.json`, no hand-written "used in"; the full spec is generated in stage 1b (section 6.1b).
21. **Stage 1b, UI building blocks:** after flows are done, before PRD-approved (section 6.1b).
22. **Design versions:** each gate pins a canvas version; later changes start from a quick message (section 6.1b).
23. **No design snapshots in the repo:** a gitignored cache for validation and builds; README screenshots from the live app (section 6.1b).
24. **The Workout Log canvas** is updated by Nik after the skill is finalized, not before.
26. **Claude Design can keep non-page files in the canvas** (tested 2026-11-15). The canvas already holds `tools/elements.py`, `uploads/prd-….md`, and the design system's `readme.md`, and the skill reads them like any other file. So `flows.md` and `elements.json` can live there. **Confirmed with a live test the same day:** Claude Design created `_test/flows.md` and `_test/elements.json`, then updated one row in each on request. The skill read both back, with contents matching Claude Design's report, and the page list, SignIn, `styles.css`, and `support.js` hashes unchanged.
27. **Template fixes from that test:** (1) the `flows.md` template needs the `|---|` line under the table header; (2) the `elements.json` template ships as a strict JSON Schema, because Claude Design put padding and type inside `sizes` when the shape was loose; (3) every element needs an ID before Claude Design writes it; (4) empty fields stay empty rather than invented (Claude Design did this unprompted), and the validator flags empty fields on Settled elements.
31. **Stage 1 instructions are defaults, not a script.** Skip categories the input already answers, keep question batches short, and don't research what Nik already decided.
32. **No scaffold template until Workout Log ships.** The plugin (skills and agents) is built stage by stage during the Workout Log build. The `template/` scaffold is generated afterward, by comparing Dunraven, the meal planner, and Workout Log. Workout Log's repo is set up by hand. This replaces decision 4's "created from the scaffold" for now.
33. **The design comparison tool is built and tuned during the Workout Log build** (D-28), with screenshot grading as the fallback.
34. **Lean subagent sessions** (section 6.5): each agent gets only the tools and MCP servers its role needs, and context per agent is measured at the first lane.
35. **This PRD is retired once the skill works.** It's replaced by a short README in the plugin repo: the north star (goals, non-goals, the pipeline, the human gates, the rules that made Dunraven work), to keep the skills in check without restating them. Details live in the skills only.
36. **The Claude Design prompt is a skill file, not generated on the fly** (2026-11-17). `plugin/skills/design-brief/` holds `brief.md` (rules R1–R13), `elements.schema.json`, and `copy-brief.sh`, which joins them and copies the result to the clipboard for Nik to paste. It's versioned (`design-brief v1`); the canvas's `flows.md` header records the version it follows, and design-sync cites rule numbers and flags an older version as a decision. Also added by the brief: a Data column per screen (the fixture, D-29), a Status table for what's final, and `data-screen` on each screen frame. Started locally at `~/Claude/Projects/idea-to-app/` (no git or GitHub yet).
37. **Stage 0 built and run** (2026-11-17). `plugin/skills/intake/SKILL.md` was run on Workout Log, now named **Superset** (`~/Claude/Projects/Superset/`). It saved the claude.ai idea chat verbatim (read through Nik's logged-in browser), copied PRD v3, recorded the canvas link and version, and wrote `intake.md` and `STATUS.md`. Lessons: page-tool output is cut off at about 1 KB per call, so long chats are read in slices; and the canvas version changes while Nik edits, so intake records the version as "at intake", not as a pin.

## 12. Distribution: the project scaffold

One public GitHub repo (working name `nikrom17/idea-to-app`) holds everything that's the same for every project. **Build order (decisions 28 and 32):** the plugin is built stage by stage during the Workout Log build; `template/` and `new-project.sh` come after Workout Log ships, shaped by comparing all three apps. The layout below is the target.

```
idea-to-app/
├── plugin/                    # the skills, packaged as a Claude Code plugin
│   └── skills/
│       ├── idea-to-app/       # master: runs the stages in order
│       ├── prd-vet/           # stage 1, including option research and flows.md
│       ├── design-brief/      # the versioned prompt pasted into Claude Design (rules R1–R13 + elements schema)
│       ├── design-sync/       # the design-sync validator (stages 1, 4, and design changes)
│       ├── ui-blocks/         # stage 1b: patterns and the element spec
│       ├── poc-triage/        # stages 2–4
│       ├── hld/               # stage 5
│       ├── build-loop/        # stages 6–9 (harness, criteria, waves, verifier)
│       └── teardown/          # stage 10
├── template/                  # copied into each new project
│   ├── app/                   # the default stack, empty but working (lint, test, build, deploy)
│   ├── docs/                  # PRD, HLD, research, flows.md, and elements templates (the last two are given to Claude Design)
│   ├── idea-to-app.config.json  # ui.fidelity, ui.tolerance_px, canvas link
│   ├── .design-cache/         # gitignored; pinned canvas version, rebuilt each run
│   ├── pocs/                  # POC doc template
│   ├── validation/            # criteria, rubric, and report templates
│   ├── .claude/agents/        # agent definition templates
│   ├── CLAUDE.md
│   └── STATUS.md
├── sanity-check/              # Dunraven and meal-planner inputs for the quick check (section 13)
└── new-project.sh             # creates a project repo from template/
```

- **Starting a project:** `new-project.sh <name>` creates a new git repo from `template/`, optionally creates its GitHub repo, and opens Claude Code there. Then run `/idea-to-app`.
- **Skills are installed once, not copied.** Install the plugin from the GitHub repo once, and every project uses the same version. A fix to a skill reaches every project after `/plugin update`. If skills were copied into each project, every copy would drift.
- **Public vs. private:**
  - **Scaffold and skills: public.** They hold no secrets or personal data.
  - **POC registry: private.** POC folders hold account names, project IDs, real personal data (calendar events, weight, activity, recipes), and the meal-plan audit found live OAuth tokens in some of them. Single POCs can be cleaned and published later.
  - **Each app** decides for itself whether it's public.

## 13. Sanity check

A quick check that the skill behaves sensibly, not a full validation process. It runs once, and Nik looks at the results.

| Case | Run | Looks right if |
|---|---|---|
| **Dunraven Manor** | Stage 1 on Nik's opening brief (`prd-step-retrospective.md` §1) | It asks to read the existing POC first, asks about offline use, source of truth, and iOS alerts, and its PRD outline is close to `party-companion-prd.md`. |
| **Meal planner** | Stage 2 on `meal-life-app-prd.md` | Its candidate list includes the POCs the audit called critical to the core feature, grouped into sensible waves. |

The real test is the next app. Nik builds it with the skill and adjusts the skill as he goes.
