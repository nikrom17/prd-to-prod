---
name: intake
description: Stage 0 of idea-to-app. Creates the project folder and STATUS.md, saves every raw input verbatim (idea chats, rough PRDs, design canvas link and version, reference pages), asks the reuse question once, and records workflow rules and hard context. Use when Nik starts a new app or says "start at the beginning" on one.
---

# Stage 0 · Intake

Goal: everything stage 1 needs is in one place, unedited, before any question or draft.

## Steps

1. **Project folder.** `~/Claude/Projects/<Name>/`, named as Nik says. Run `git init` locally only; no GitHub repo until Nik asks. Don't move or delete earlier folders the inputs came from. Copy from them instead.
2. **Save raw inputs verbatim** into `inputs/`, one file each, never edited afterward:
   - **Chats** (`inputs/chat-<slug>.md`): the full conversation along the current branch, both sides. For a claude.ai link, read it through Nik's logged-in browser (`/api/organizations/<org>/chat_conversations/<id>?tree=True&rendering_mode=messages`, then follow `current_leaf_message_uuid` back to the root). Keep text blocks as they are. Replace tool calls with `_[tool: name]_`, drop tool results, and strip URL query strings. Put the source link and date at the top.
   - **Docs** (PRDs, notes): copy the file as it is, as `inputs/<original-name>`.
   - **Design canvas** (`inputs/design-canvas.md`): link, the version ID and file count at intake, and the list of pages. Don't copy design files (decision 23).
   - **Reference pages** (Notion, Docs): link plus what each one is for. Stage 1 reads them in full.
3. **Ask once:** "Is there existing code, a POC, design docs, data sources, or a platform you want to reuse?" Add anything named to step 2. Check the POC registry for matches.
4. **Write `intake.md`:**
   - **North star:** Nik's own words for the goal, quoted from the inputs with a pointer to each source. No paraphrase.
   - **Inputs:** a table of each file, what it is, and its date. Note which input is newest when inputs disagree; stage 1 reconciles them, intake doesn't.
   - **Workflow rules:** the gates (section 6 of the north star), what counts as approval ("approved" in words; praise isn't approval), and where files may be written.
   - **Hard context:** deadline, devices, environment (connectivity), and content rules (privacy, brand). Write "unknown" instead of guessing, and add each unknown to the stage 1 question list.
   - **Decisions:** the section 6.0 format. Intake only records decisions Nik made during intake (like the project name).
5. **`STATUS.md`:** the stage table (0–10) with state and output links, the current stage, and the next action. Every later stage updates it.
6. **Commit** `Intake: <name>` locally, then tell Nik what was saved and what stage 1 will ask about first.

## Don't

- Don't draft, fix, or reformat the PRD, even when inputs conflict. That's stage 1.
- Don't change the design canvas or the reference pages.
- Don't copy secrets into `inputs/`. If an input contains a token or password, save it with that value redacted and tell Nik.
