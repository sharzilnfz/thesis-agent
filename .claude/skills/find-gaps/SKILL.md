---
name: find-gaps
description: Run adversarial stress-testing over the approved literature to identify research gaps (Gate 3).
disable-model-invocation: false
---

# Gap Identification & Adversarial Falsification Workflow

Execute this workflow to stress-test claims and discover open research niches:

1. **Step 1: Inspect Current Claims**
   - Read `data/evidence_ledger.json` and extract the primary findings or assertions made by included papers.

2. **Step 2: Dispatch Adversarial Queries**
   - For each primary claim, run counter-queries to search for refutations or identified failure modes:
     ```bash
     python scripts/scholar_search.py --query "<claim_topic> limitation rebuttal failure" --limit 3
     ```

3. **Step 3: Update `data/gaps.json` (Gate 3)**
   - Record conflicting evidence, unaddressed edge cases, or dataset limitations.
   - Present findings to the user:
     - *Claim A vs. Contradiction B*
     - *Identified Open Problem / Defensible Thesis Angle*
   - Ask the user to confirm the focal research gap before drafting begins.
