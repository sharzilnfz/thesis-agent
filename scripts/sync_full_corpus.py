#!/usr/bin/env python3
"""
Synchronize all 93 PDFs in data/raw_papers/ into data/papers.json and paper/references.bib.
Ensures every PDF has a canonical bibtex_key, resolved pdf_path, and metadata.

Implements principle-build-the-lever and principle-prove-it-works.
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_JSON = REPO_ROOT / "data" / "papers.json"
CORPUS_SUMMARY_JSON = REPO_ROOT / "data" / "corpus_summary.json"
FINAL_STATUS_JSON = REPO_ROOT / "data" / "raw_papers" / "_FINAL_STATUS.json"
BIB_FILE = REPO_ROOT / "paper" / "references.bib"
RAW_DIR = REPO_ROOT / "data" / "raw_papers"


def clean_bib_key(title: str, filename: str, existing_keys: set) -> str:
    # Try to extract author and year from filename or title
    m = re.search(r"(\d{2})_([A-Za-z]+)_.*?(\d{4})", filename)
    if m:
        author = m.group(2).lower()
        year = m.group(3)
    else:
        # fallback parsing
        m_year = re.search(r"\b(20\d\d|19\d\d)\b", filename)
        year = m_year.group(1) if m_year else "2024"
        words = re.findall(r"[A-Za-z]+", filename)
        author = words[0].lower() if words else "author"

    title_words = re.findall(r"[A-Za-z]+", title)
    kw = title_words[0].lower() if title_words else "paper"
    if kw.lower() in ["a", "an", "the", "on"] and len(title_words) > 1:
        kw = title_words[1].lower()

    base_key = f"{author}{year}{kw}"
    cand = base_key
    suffix = ord("b")
    while cand in existing_keys:
        cand = f"{base_key}{chr(suffix)}"
        suffix += 1
    existing_keys.add(cand)
    return cand


def main():
    if not CORPUS_SUMMARY_JSON.exists():
        print(f"[-] {CORPUS_SUMMARY_JSON} missing.")
        return

    with open(CORPUS_SUMMARY_JSON, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    existing_papers = {}
    if PAPERS_JSON.exists():
        try:
            with open(PAPERS_JSON, "r", encoding="utf-8") as f:
                existing_papers = json.load(f)
        except Exception:
            existing_papers = {}

    existing_keys = {
        p.get("bibtex_key")
        for p in existing_papers.values()
        if p.get("bibtex_key")
    }

    # Map filename to existing paper if already registered
    filename_to_key = {}
    for p in existing_papers.values():
        path = p.get("pdf_path")
        if path:
            filename_to_key[Path(path).name] = p.get("bibtex_key")

    new_count = 0
    updated_count = 0

    for item in corpus:
        fname = item["filename"]
        pdf_path = RAW_DIR / fname
        if not pdf_path.exists():
            continue

        rel_pdf = str(pdf_path.relative_to(REPO_ROOT))
        title = item.get("title") or fname.replace(".pdf", "")

        # Find or create canonical ID
        canonical_id = f"local:{fname.replace('.pdf', '')}"

        # Match with existing entry if present
        matched_existing = None
        for pid, ep in existing_papers.items():
            if ep.get("pdf_path") == rel_pdf or ep.get(
                "title", ""
            ).lower() == title.lower():
                matched_existing = pid
                break

        if matched_existing:
            existing_papers[matched_existing]["pdf_path"] = rel_pdf
            existing_papers[matched_existing]["screening_status"] = "approved"
            existing_papers[matched_existing]["category"] = item.get("category")
            existing_papers[matched_existing]["abstract"] = (
                item.get("abstract")
                or existing_papers[matched_existing].get("abstract", "")
            )
            updated_count += 1
        else:
            bib_key = clean_bib_key(title, fname, existing_keys)
            existing_papers[canonical_id] = {
                "id": canonical_id,
                "title": title,
                "authors": [fname.split("_")[1]] if "_" in fname else ["Anon"],
                "year": int(re.search(r"\b(20\d\d)\b", fname).group(1))
                if re.search(r"\b(20\d\d)\b", fname)
                else 2024,
                "venue": item.get("category", "WiFi Sensing"),
                "bibtex_key": bib_key,
                "abstract": item.get("abstract", ""),
                "pdf_path": rel_pdf,
                "screening_status": "approved",
                "category": item.get("category"),
                "screening_reason": f"Core corpus paper ({item.get('category')})",
            }
            new_count += 1

    with open(PAPERS_JSON, "w", encoding="utf-8") as f:
        json.dump(existing_papers, f, indent=2, ensure_ascii=False)

    # Rebuild references.bib cleanly
    bib_entries = []
    for pid, p in existing_papers.items():
        key = p.get("bibtex_key")
        if not key:
            continue
        title = p.get("title", "Untitled").replace("{", "").replace("}", "")
        authors = ", ".join(p.get("authors", ["Unknown"]))
        year = p.get("year", 2024)
        venue = p.get("venue", "arXiv")
        entry = (
            f"@article{{{key},\n"
            f"  title={{{title}}},\n"
            f"  author={{{authors}}},\n"
            f"  journal={{{venue}}},\n"
            f"  year={{{year}}}\n"
            f"}}"
        )
        bib_entries.append(entry)

    with open(BIB_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(bib_entries) + "\n")

    print(
        f"[+] Synchronized corpus: {len(existing_papers)} total papers ({new_count} newly added, {updated_count} updated)."
    )
    print(f"[+] Rebuilt {BIB_FILE.relative_to(REPO_ROOT)} with {len(bib_entries)} entries.")


if __name__ == "__main__":
    main()
