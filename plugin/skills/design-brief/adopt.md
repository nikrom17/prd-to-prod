# Adopt the brief · design-brief v1

Paste this after the brief, once you've read the agent's list of gaps.

---

Bring this canvas in line with design-brief v1. Fix every gap you listed, except anything I ruled out below. Restructure only; don't change how any screen looks or behaves.

1. **`flows.md`** at the canvas root (R1–R5): one row per screen for every screen on the canvas, using the existing screen IDs and captions. Move the decision log ("what's locked", "still open") into its Decisions section. Locked items become Decided with a one-line Outcome. Still-open items stay Open, with options if the canvas shows them.
2. **Data column:** fill it in wherever the screen makes the state clear. Leave `-` where it doesn't. Don't guess.
3. **Status table (R4):** add a row for each flow, marked **Final** if I've told you it's done, otherwise **In progress**. Don't decide this yourself. If you aren't sure, mark it In progress and list it in your reply.
4. **`elements.json`** following the schema (R7–R8), built from the current Elements page. Mark elements `settled` only if the Elements page or I say so. Leave unknown fields out.
5. **Tokens (R11):** move raw values into `styles.css` tokens. Where two values conflict (for example, the accent `oklch(0.62 0.21 35)` on the Final page vs `#ec3013` in the token sheet), don't pick one: add a decision.
6. **Screen frames and captions (R12–R13).** Add `data-screen` to every screen. Add the R10 tags to Settled elements now; Draft elements can wait until they're settled.
7. **Delete `_test/`.** It was a format test.

When you're done, reply with only:
- the files you changed or created
- each flow and its Status
- the open decisions
- anything you couldn't do, and why
