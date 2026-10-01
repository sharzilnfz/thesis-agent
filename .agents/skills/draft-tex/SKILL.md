---
name: draft-tex
description: Synthesize thesis sections in LaTeX and validate via deterministic citation auditing (Gate 4).
disable-model-invocation: false
---

# LaTeX Chapter Drafting Workflow

Execute this workflow to draft a thesis section and enforce citation integrity:

1. **Step 1: Check Ledger Backing**
   - Read `data/evidence_ledger.json` and ensure claims to be written have verified passage quotes and BibTeX keys.

2. **Step 2: Draft Chapter Content**
   - Use the `@writer` persona to generate LaTeX content into `paper/chapters/ch<N>_<title>.tex`.
   - Ensure every `\cite{key}` references a key in `paper/references.bib`.

3. **Step 3: Run Deterministic Gatekeeper (Gate 4)**
   - Run the audit script:
     ```bash
     python scripts/verify_bibtex.py
     ```
   - If the script fails, inspect missing keys and either add the missing ledger passage or adjust the citation.
   - Present the final compiled chapter diff to the user for review.
