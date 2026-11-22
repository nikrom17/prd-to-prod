# Migrate v1 → v2, step 2: apply · design-brief v2

Send after Nik approves the mapping table (with any edits he typed).

---

Apply the mapping table you proposed, with any changes I've written above. Restructure only; don't change how any screen looks or behaves.

1. **`flows.md`:** set the header to `brief: design-brief v2`, renumber the flow and sub-flow headings, and add `#` and `Name` columns to every table (R2). Renumber edge cases (R3). Update every screen reference in steps, edge cases, decisions, and Status. Move demo pages to "Pages" (R14). Add the **Former IDs** table at the end.
2. **Canvas:** on every screen, set `data-screen` to the new number and add `data-name`. Every caption starts with the new number (R12–R13).
3. **`elements.json`:** set `"brief": "design-brief v2"`, and replace former screen or section references in rules and notes (like "(35b)") with new numbers. Where a reference points at the archived page, write "archived" instead.
4. Regenerate the Elements page.

When you're done, reply with only: the files you changed, the flow list with new numbers, and anything you couldn't map.
