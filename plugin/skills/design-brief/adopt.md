# Adopt the brief · design-brief v2

Paste this after the brief, once you've read the agent's list of gaps.

---

Bring this canvas in line with design-brief v2. Fix every gap you listed. Restructure only; don't change how any screen looks or behaves.

0. **Scope:** the current pages are {{CURRENT_PAGES}}. Every other design page is archived: add "Archived, not part of the spec" to its title, and leave it out of `flows.md`, the tags, and the token work. Don't delete it.

1. **`flows.md`** at the canvas root (R1–R5): one row per screen for every screen on the current pages, using the existing screen IDs and captions. Move the decision log ("what's locked", "still open") into its Decisions section. Locked items become Decided with a one-line Outcome. Still-open items stay Open, with options if the canvas shows them.
2. **Data column:** fill it in wherever the screen makes the state clear. Leave `-` where it doesn't. Don't guess.
3. **Status table (R4):** add a row for each flow, marked **Final** if I've told you it's done, otherwise **In progress**. Don't decide this yourself. If you aren't sure, mark it In progress and list it in your reply.
4. **`elements.json`** following the schema (R7–R8), built from the current Elements page. Give every element an ID. Mark elements `settled` only if the Elements page or I say so. Leave unknown fields out.
   - **The Elements page stays, rendered from `elements.json`** (update the generator to read it). Drop its "Used in" and height-check columns, because the pipeline generates and checks those. Open issues from its issues column become decisions in `flows.md`, and fixed issues are dropped.
5. **Tokens (R11), all of them now:** colors, type (add type tokens such as `--type-button`), spacing, radius, shadows, and scrims, defined once in `styles.css`. Define any token that screens use but `styles.css` doesn't define. Where two definitions conflict (for example, the hex values in `styles.css` vs the OKLCH overrides on the current page, or theme variants), don't pick one: add a decision, and keep the current look until it's decided. List any value you couldn't map to a token.
6. **Screen frames and captions (R12–R13).** Add `data-screen` to every screen. Add the R10 tags to Settled elements now; Draft elements can wait until they're settled.
7. **Delete `_test/`.** It was a format test.

When you're done, reply with only:
- the files you changed or created
- each flow and its Status
- the open decisions
- anything you couldn't do, and why
