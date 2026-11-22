# GitHub setup: prd-to-prod and Superset

Status: **All decided**, 2026-11-22. Nothing has been pushed yet. The one remaining step is `! gh auth login` (G-01).

## Both repos

### G-01 · Who creates the GitHub repos        Status: Decided
Nik: yes, install gh CLI
Outcome: `gh` 2.104.0 is installed with Homebrew. **You need to run `! gh auth login` once** (choose GitHub.com, SSH, and your existing key). After that, I create repos with `gh`, including for future apps.

### G-02 · Remote protocol        Status: Decided
Outcome: SSH, the same as Dunraven (accepted).

### G-03 · Commit author email        Status: Decided
Nik: keep it public
Outcome: Commits keep `Nik Roman` with your Gmail, in both repos.

### G-04 · Claude attribution        Status: Decided
Nik: remove co-authored... it's kind of a given since this is a Claude skill
Outcome: Removed from both repos' commits (amended before any push). Future commits don't add it (saved as a preference).

### G-05 · Branch protection        Status: Decided
Nik: what are you proposing for branch protection?
Options:
(a) **Minimal:** on `main`, block force-pushes and deletion. No pull-request requirement, so you and the lead build agent push directly, the way Dunraven worked. From stage 8, a GitHub Actions run (lint, unit tests, build) on every push gives a red or green badge but doesn't block. The real gate stays the independent verifier.
(b) **PR-gated:** every change goes through a pull request with required CI checks. It's safer against a bad push, but every agent merge becomes a PR, which slows the build loop and adds cost for a solo project.
(c) **None.**
Recommend: (a). The verifier, the frozen criteria, and the integrity diff already catch weakened tests and bad merges. Branch protection only has to stop history from being lost.
Nik: okay
Outcome: (a), 2026-11-22, on both repos.

## prd-to-prod (the skills)

### G-06 · Name        Status: Decided
Nik: give me 3 alternative names
Options:
(a) `idea-to-app` (current): matches the skill's input and output.
(b) `prd-to-prod`: PRD in, production out. Uses the words you already use.
(c) `spec-to-ship`: a familiar phrase, and not tied to "PRD".
(d) `proven-build`: names what makes it different, that every requirement is proven by an independent verifier.
Recommend: (a) or (b). The skill's commands carry the name (`/idea-to-app:intake`), so shorter and plainer reads better.
Nik: prd-to-prod
Outcome: `nikrom17/prd-to-prod`, 2026-11-22. The local folder is now `~/Claude/Projects/prd-to-prod/`, and every reference in the skills, the skill PRD, Superset, and memory was renamed. Commands will be `/prd-to-prod:intake` and so on.

### G-07 · Visibility        Status: Decided
Outcome: Public (accepted).

### G-08 · Description        Status: Decided
Outcome: "Claude Code plugin: take an idea, chat, or rough PRD to a verified, deployed app (PRD → POCs → HLD → frozen criteria → independent verifier)." (accepted)

### G-09 · What gets pushed        Status: Decided
Nik: the PRD is done for the skill, right? I would move that now
Outcome: Yes. Every decision in it is Decided. It moved to `docs/skill-prd.md` in this repo, and memory points there. It stays the working spec until the skill works, then it's replaced by the north-star README (decision 35). Its source notes (`prd-to-app-process.md`, `prd-step-retrospective.md`, `poc-plan.md`) stay in the meal-plan folder until housekeeping; the PRD's header says where they are.

### G-10 · README and license        Status: Decided
Nik: MIT is fine for the skill
Outcome: `LICENSE` (MIT, © 2026 Nik Roman) added. A placeholder README gets added with the first push.

### G-11 · What "plugin" means here        Status: Decided
Nik: what is a plugin in this context?
A **Claude Code plugin** is a folder with a small manifest (`.claude-plugin/plugin.json`) that bundles skills, subagent definitions (like the verifier and builder), slash commands, and hooks. You install it once per computer from a git repo with `/plugin install`. From then on it works in every project (for example `/idea-to-app:intake`), and `/plugin update` pulls the latest version from GitHub.
Why it fits: one copy of the skill for all apps (decision 8), with versions coming from git history. The alternative is copying the skill folders into `~/.claude/skills/`, which works but doesn't carry the agent definitions or version updates.
Recommend: add the manifest once stages 0–1b are working on Superset. Until then I run the skills directly from this folder.
Nik: does this mean it's officially published? Could it get GitHub stars?
Outcome: Answered. Stars come from the repo being public, which happens at the first push, with or without a plugin. The manifest only makes it installable. Anyone who finds the repo can run `/plugin marketplace add nikrom17/prd-to-prod`. Being listed in Anthropic's own plugin directory is a separate submission you'd choose to make later. The manifest still gets added once stages 0–1b work.

## Superset (the app)

### G-12 · Name        Status: Decided
Outcome: `nikrom17/superset` (accepted).

### G-13 · Visibility        Status: Decided
Nik: naw, make it public. idk if I want chat history committed though. I just want the product requirements and assets committed.
Outcome: Public. What gets committed is G-17.

### G-14 · Description        Status: Decided
Outcome: "Gym logbook PWA: a target for every set, progressive overload toward your trainer's plan, logging that works offline." (accepted)

### G-15 · What gets pushed        Status: Decided
Outcome: Depends on G-17.

### G-16 · Hosting        Status: Decided
Outcome: Nothing until stage 6 (accepted).

### G-17 · The inputs folder in a public repo        Status: Decided
Source: G-13. Today `inputs/` holds the idea chat (your words, workout weights, and file paths), PRD v3, and the canvas pointer.
Proposal:
1. **Committed:** product requirements and their pointers: `intake.md`, `STATUS.md`, `inputs/workout-log-app-prd.md`, and `inputs/design-canvas.md`.
2. **Not committed:** `private/`, which is gitignored. It holds the idea chat (`private/chat-idea.md`), kept on disk so stage 1 can still read it word for word.
3. **`intake.md`** keeps the north-star quotes (they're requirements in your own words), with the source shown as "idea chat (private)".
4. **History:** the chat is in the unpushed commit `fb28f4c`. I rewrite that commit so the chat never reaches GitHub (and drop the co-author line, G-04).
5. **Later (heads-up):** your real workout history from Notion is personal data, so it goes in `private/` as well. The fixture library (D-29) that tests and the `/gallery` use is made-up data, so the public repo never holds your real sessions.
6. **The skill changes to match:** intake saves chats to `private/` by default, and asks once whether the repo will be public.
Question on "assets": today the design stays in the canvas, and the repo only holds the link (decision 23, to avoid two copies drifting). App assets like icons and images get committed with the app code at stage 6. Did you mean those, or do you want the design files themselves in the repo?
Nik: I think there should be some screenshots of the designs curated for GitHub, maybe not a raw design file
Outcome: Proposal 1–6 done, 2026-11-22. The chat is in `private/` (gitignored), commit `fb28f4c` was rewritten as `cc87f5b` without the chat, and the intake skill now defaults to `private/`. **Plus curated screenshots:** when you mark a design version final, the screens you pick are rendered from that pin to `docs/design/<version>/<screen-id>.png` and committed. They're screenshots, not design files, and never edited. The canvas isn't final yet, so the first push has none. Skill decision 39.

## Out of scope here

- Renaming `meal-plan-auto-scheduler` → `dunraven-manor`, and the rest of housekeeping. That's still last and needs your go-ahead.
- The private `poc-registry` repo (skill decision 2). It's created when stage 2 first needs it.
