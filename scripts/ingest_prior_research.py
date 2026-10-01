#!/usr/bin/env python3
"""
Ingest prior research matrix and expanded papers into ThesisAgent data structures:
- data/papers.json
- paper/references.bib

Implements principle-build-the-lever and principle-laziness-protocol.
"""
import csv
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_PATH = REPO_ROOT / "data" / "papers.json"
BIB_PATH = REPO_ROOT / "paper" / "references.bib"
MATRIX_PATH = REPO_ROOT / "wifi-csi-thesis" / "latestAgents" / "wifi_csi_literature_matrix.csv"


def clean_bibtex_key(author: str, year: str, title: str, existing_keys: set) -> str:
    author_clean = re.sub(r"[^a-zA-Z]", "", author.split()[-1].lower()) if author else "anon"
    words = [re.sub(r"[^a-zA-Z]", "", w.lower()) for w in title.split() if w]
    word_clean = words[0] if words else "paper"
    year_digits = re.search(r"\b(20\d\d|19\d\d)\b", str(year))
    year_str = year_digits.group(1) if year_digits else "2025"
    base_key = f"{author_clean}{year_str}{word_clean}"

    candidate_key = base_key
    suffix_char = ord("b")
    while candidate_key in existing_keys:
        candidate_key = f"{base_key}{chr(suffix_char)}"
        suffix_char += 1
    existing_keys.add(candidate_key)
    return candidate_key


def parse_matrix_csv():
    if not MATRIX_PATH.exists():
        return []
    records = []
    with open(MATRIX_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def main():
    PAPERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    BIB_PATH.parent.mkdir(parents=True, exist_ok=True)

    papers = {}
    if PAPERS_PATH.exists():
        try:
            with open(PAPERS_PATH, "r", encoding="utf-8") as f:
                papers = json.load(f)
        except Exception:
            papers = {}

    existing_keys = {p.get("bibtex_key") for p in papers.values() if p.get("bibtex_key")}

    # Ingest from CSV matrix
    matrix_rows = parse_matrix_csv()
    added_count = 0

    for row in matrix_rows:
        title = row.get("title", "").strip()
        if not title:
            continue

        url = row.get("source_url", "").strip()
        theme = row.get("theme", "").strip()
        year_note = row.get("year_note", "").strip()
        venue = row.get("venue_or_status", "").strip()
        priority = row.get("priority", "").strip()
        what_to_build_on = row.get("what_to_build_on", "").strip()
        limitations = row.get("limitation_or_check", "").strip()

        # Parse arXiv ID or DOI from URL
        arxiv_match = re.search(r"arxiv\.org/(?:abs|html|pdf)/([0-9]+\.[0-9]+)", url)
        arxiv_id = f"arxiv:{arxiv_match.group(1)}" if arxiv_match else ""

        doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", url)
        doi = f"doi:{doi_match.group(0)}" if doi_match else ""

        reading_id = row.get("reading_id", "").strip()
        canonical_id = doi or arxiv_id or f"matrix:{reading_id}:{title[:20].lower()}"

        if canonical_id in papers:
            continue

        first_author = "author"
        bib_key = clean_bibtex_key(first_author, year_note, title, existing_keys)

        papers[canonical_id] = {
            "id": canonical_id,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": [first_author],
            "year": int(re.search(r"\b(20\d\d|19\d\d)\b", year_note).group(1)) if re.search(r"\b(20\d\d|19\d\d)\b", year_note) else 2025,
            "venue": venue,
            "bibtex_key": bib_key,
            "abstract": f"Theme: {theme}. Focus: {what_to_build_on}. Limitation: {limitations}",
            "pdf_path": None,
            "screening_status": "candidate",
            "screening_reason": f"Ingested from prioritized matrix ({priority})",
            "metadata": {
                "source_url": url,
                "theme": theme,
                "priority": priority,
                "what_to_build_on": what_to_build_on,
                "limitation_or_check": limitations,
            },
        }
        added_count += 1

    with open(PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    # Append new BibTeX entries to references.bib
    existing_bib_content = ""
    if BIB_PATH.exists():
        with open(BIB_PATH, "r", encoding="utf-8") as f:
            existing_bib_content = f.read()

    new_bib_entries = []
    for p in papers.values():
        key = p.get("bibtex_key")
        if not key or f"{{{key}," in existing_bib_content:
            continue
        entry = (
            f"@article{{{key},\n"
            f"  title={{{p.get('title')}}},\n"
            f"  author={{{', '.join(p.get('authors', ['Unknown']))}}},\n"
            f"  journal={{{p.get('venue') or 'arXiv'}}},\n"
            f"  year={{{p.get('year')}}},\n"
            f"  url={{{p.get('metadata', {}).get('source_url', '')}}}\n"
            f"}}\n"
        )
        new_bib_entries.append(entry)

    if new_bib_entries:
        with open(BIB_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(new_bib_entries))

    print(f"[+] Ingested {added_count} papers from literature matrix. Total in corpus: {len(papers)}")
    print(f"[+] Appended {len(new_bib_entries)} entries to {BIB_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
