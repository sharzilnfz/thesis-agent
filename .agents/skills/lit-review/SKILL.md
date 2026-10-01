---
name: lit-review
description: Harvest literature from arXiv and Semantic Scholar, screen candidates, and steer through Gates 1 & 2.
disable-model-invocation: false
---

# Literature Review Workflow

Execute this workflow when conducting a literature search pass:

1. **Step 1: Check Scope (Gate 1)**
   - Read `program.md` to identify the current research questions and milestones.
   - Formulate 2–3 targeted queries (combining domain terms + benchmark names).
   - Ask the user: *"Proposed queries are [X, Y, Z]. Approve or refine?"*

2. **Step 2: Harvest Literature**
   - Execute the harvesting script:
     ```bash
     python scripts/scholar_search.py --query "<approved_query>" --limit 5
     ```
   - Read `data/papers.json` to inspect the newly discovered papers.

3. **Step 3: Corpus Review (Gate 2)**
   - Display a clean summary table of newly discovered papers (Title, Authors, Year, Venue, Abstract summary).
   - Prompt the user: *"Which of these should be included in the active corpus? Any to exclude?"*
   - Update `screening_status` in `data/papers.json` based on the user's response.
