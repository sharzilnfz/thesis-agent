#!/usr/bin/env python3
"""
Deterministic Gatekeeper: Audits LaTeX files in paper/chapters/ and paper/main.tex
against paper/references.bib and data/evidence_ledger.json.

Validations:
- Supports \\cite{}, \\citet{}, \\citep{}, \\autocite{}, \\parencite{}, \\textcite{}
- Scans both paper/main.tex and paper/chapters/*.tex
- Handles dict-of-dicts and list-of-dicts ledger formats
- Enforces passage existence, minimum length, and valid page number
- Exits with code 1 if any violation is detected
"""
import os
import re
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_TEX_PATH = REPO_ROOT / "paper" / "main.tex"
CHAPTERS_DIR = REPO_ROOT / "paper" / "chapters"
BIBTEX_PATH = REPO_ROOT / "paper" / "references.bib"
LEDGER_PATH = REPO_ROOT / "data" / "evidence_ledger.json"

CITE_REGEX = re.compile(
    r"\\(?:cite|citep|citet|autocite|parencite|textcite)(?:\[.*?\])*\{([^}]+)\}"
)

def extract_citations_from_file(file_path: Path) -> set:
    citations = set()
    if not file_path.exists():
        return citations
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("%"):
                continue
            matches = CITE_REGEX.findall(line_str)
            for m in matches:
                for key in m.split(","):
                    clean_key = key.strip()
                    if clean_key:
                        citations.add(clean_key)
    return citations

def extract_all_tex_citations() -> set:
    citations = set()
    # 1. Scan main.tex
    citations.update(extract_citations_from_file(MAIN_TEX_PATH))
    # 2. Scan all chapter files
    if CHAPTERS_DIR.exists():
        for f in CHAPTERS_DIR.glob("*.tex"):
            citations.update(extract_citations_from_file(f))
    return citations

def load_bibtex_keys(bib_path: Path) -> set:
    keys = set()
    if not bib_path.exists():
        return keys
    key_pattern = re.compile(r"@\w+\s*\{\s*([^,]+),")
    with open(bib_path, "r", encoding="utf-8") as f:
        for line in f:
            match = key_pattern.match(line.strip())
            if match:
                keys.add(match.group(1).strip())
    return keys

def load_and_validate_ledger(ledger_path: Path) -> dict:
    """
    Returns a mapping of bibtex_key -> list of evidence entries.
    Validates passage non-empty, min length 15 chars, and page_number > 0.
    """
    if not ledger_path.exists():
        return {}
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return {}

    entries = []
    if isinstance(raw, dict):
        entries = list(raw.values())
    elif isinstance(raw, list):
        entries = raw

    key_to_entries = {}
    for item in entries:
        bkey = item.get("bibtex_key")
        if not bkey:
            continue
        key_to_entries.setdefault(bkey, []).append(item)
    return key_to_entries

def main():
    tex_cites = extract_all_tex_citations()
    bib_keys = load_bibtex_keys(BIBTEX_PATH)
    ledger_map = load_and_validate_ledger(LEDGER_PATH)

    print(f"[*] Auditing {len(tex_cites)} citations across paper/main.tex and chapters/*.tex...")
    
    missing_in_bib = tex_cites - bib_keys
    missing_in_ledger = tex_cites - set(ledger_map.keys())

    errors = 0
    if missing_in_bib:
        print(f"[-] ERROR: Citations missing from {BIBTEX_PATH.name}:")
        for k in sorted(missing_in_bib):
            print(f"    - \\cite{{{k}}}")
        errors += 1

    if missing_in_ledger:
        print(f"[-] ERROR: Citations lacking entries in {LEDGER_PATH.name}:")
        for k in sorted(missing_in_ledger):
            print(f"    - \\cite{{{k}}}")
        errors += 1

    # Quality check on ledger entries
    for cite_key in tex_cites:
        if cite_key in ledger_map:
            for ev in ledger_map[cite_key]:
                passage = ev.get("exact_passage", "").strip()
                page = ev.get("page_number", 0)
                if len(passage) < 15:
                    print(f"[-] ERROR: Ledger passage for '{cite_key}' too short (<15 chars).")
                    errors += 1
                if not isinstance(page, int) or page <= 0:
                    print(f"[-] ERROR: Ledger entry for '{cite_key}' has invalid page number: {page}")
                    errors += 1

    if errors > 0:
        print(f"\n[-] GATE 4 AUDIT FAILED with {errors} violations. Draft cannot be finalized.")
        sys.exit(1)

    print("[+] GATE 4 AUDIT PASSED: All citations are in .bib, verified in Evidence Ledger, and pass passage quality checks.")
    sys.exit(0)

if __name__ == "__main__":
    main()
