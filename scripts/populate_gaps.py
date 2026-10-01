#!/usr/bin/env python3
"""
Populate data/gaps.json from thesis_claim_audit.csv and adversarial review findings.
Implements principle-build-the-lever and principle-prove-it-works.
"""
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    REPO_ROOT
    / "wifi-csi-thesis"
    / "research audits with perplexity"
    / "thesis_claim_audit.csv"
)
GAPS_PATH = REPO_ROOT / "data" / "gaps.json"


def main():
    if not CSV_PATH.exists():
        print(f"[-] Error: {CSV_PATH} does not exist.")
        return

    gaps = []
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            claim_id = row.get("claim_id", "").strip()
            claim = row.get("claim", "").strip()
            verdict = row.get("verdict", "").strip()
            replacement = row.get("replacement", "").strip()
            required_check = row.get("required_check", "").strip()
            url = row.get("primary_url", "").strip()
            citation = row.get("source_citation", "").strip()

            gap_entry = {
                "gap_id": claim_id,
                "naive_claim": claim,
                "audit_verdict": verdict,
                "scientific_replacement": replacement,
                "validation_requirement": required_check,
                "source_reference": citation or url,
                "url": url,
                "status": "unresolved_until_evaluated",
            }
            gaps.append(gap_entry)

    with open(GAPS_PATH, "w", encoding="utf-8") as f:
        json.dump(gaps, f, indent=2, ensure_ascii=False)

    print(f"[+] Successfully wrote {len(gaps)} audited gaps to {GAPS_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
