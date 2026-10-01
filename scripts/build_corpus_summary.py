#!/usr/bin/env python3
"""
Corpus indexer and deep metadata extractor for all 93 PDFs in data/raw_papers/.
Merges PyMuPDF extracted abstracts, introductions, and conclusions with
the 55 curated paper analyses from wifi-csi-thesis/data_expanded_*.py.

Outputs:
- data/corpus_summary.json
- data/corpus_summary.md
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    import pymupdf as fitz

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(REPO_ROOT / "wifi-csi-thesis"))

try:
    import data_expanded_1
    import data_expanded_2
    import data_expanded_3
    import data_expanded_4

    EXPANDED_DATA = {
        item[0]: {
            "problem": item[1],
            "hard": item[2],
            "did": item[3],
            "results": item[4],
            "status": item[5],
            "effectiveness": item[6],
            "future": item[7],
        }
        for item in (
            data_expanded_1.BATCH1
            + data_expanded_2.BATCH2
            + data_expanded_3.BATCH3
            + data_expanded_4.BATCH4
        )
    }
except Exception as e:
    print(f"[-] Warning: Failed to load expanded batches: {e}")
    EXPANDED_DATA = {}


def extract_pdf_core(pdf_path: str):
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    p1_text = doc[0].get_text("text") if page_count > 0 else ""
    p2_text = doc[1].get_text("text") if page_count > 1 else ""

    # Clean text
    combined_head = p1_text + "\n" + p2_text

    # Extract Title (typically first non-empty lines)
    lines = [l.strip() for l in p1_text.splitlines() if l.strip()]
    title_cand = ""
    for l in lines[:5]:
        if len(l) > 15 and not any(
            skip in l.lower()
            for skip in ["arxiv", "vol.", "ieee", "acm", "http", "doi", "copyright"]
        ):
            title_cand = l
            break
    if not title_cand and lines:
        title_cand = lines[0]

    # Extract Abstract
    abstract = ""
    lower_comb = combined_head.lower()
    abs_pos = lower_comb.find("abstract")
    if abs_pos != -1:
        # find where abstract ends (e.g. keywords, introduction, 1. , i. )
        rest = combined_head[abs_pos + len("abstract") :]
        # strip common leading symbols
        rest = re.sub(r"^[\s—:\.\-]+", "", rest)
        end_matches = [
            m.start()
            for m in re.finditer(
                r"\b(index terms|keywords|1\.\s+introduction|i\.\s+introduction|1\s+introduction)\b",
                rest,
                re.IGNORECASE,
            )
        ]
        if end_matches:
            abstract = rest[: min(end_matches)].strip()
        else:
            abstract = rest[:1500].strip()

    # Clean multi-line abstract
    abstract = " ".join(abstract.split())

    # Extract Conclusion (last page or second-to-last)
    conclusion = ""
    for pno in range(max(0, page_count - 2), page_count):
        ptxt = doc[pno].get_text("text")
        lower_ptxt = ptxt.lower()
        conc_pos = lower_ptxt.find("conclusion")
        if conc_pos != -1:
            rest_c = ptxt[conc_pos + len("conclusion") :]
            rest_c = re.sub(r"^[\s—:\.\-]+", "", rest_c)
            ref_pos = rest_c.lower().find("references")
            if ref_pos != -1:
                conclusion = rest_c[:ref_pos].strip()
            else:
                conclusion = rest_c[:1200].strip()
            break
    conclusion = " ".join(conclusion.split())

    return {
        "title": title_cand,
        "pages": page_count,
        "abstract": abstract[:1200],
        "conclusion": conclusion[:1000],
    }


def categorize_paper(fname: str, title: str, abstract: str, expanded_info: dict) -> str:
    text = (fname + " " + title + " " + abstract + " " + str(expanded_info)).lower()

    if any(k in text for k in ["survey", "tutorial", "review"]):
        return "Survey & Foundations"
    if any(
        k in text
        for k in [
            "vital sign",
            "respiration",
            "breathing",
            "heart rate",
            "heartbeat",
            "farsense",
            "phasebeat",
            "tensorbeat",
            "pulsefi",
            "vitalcsi",
            "cardiofi",
        ]
    ):
        return "Vital Signs & Respiration"
    if any(
        k in text
        for k in [
            "generalizability",
            "domain generalization",
            "cross-domain",
            "unseen environment",
            "airfi",
            "widar3",
            "dgsense",
            "crosssense",
            "transfer",
            "am-fm",
        ]
    ):
        return "Domain Generalization & Transfer"
    if any(
        k in text
        for k in [
            "biometric",
            "person identification",
            "re-identification",
            "intruder",
            "open-set",
            "caution",
            "breathid",
            "whofi",
            "argus",
            "wiper81",
            "authentication",
            "static person",
        ]
    ):
        return "Occupant Identity & Biometrics"
    if any(
        k in text
        for k in [
            "fall detection",
            "motion detection",
            "presence",
            "welfare",
            "elderly",
            "widetect",
            "rt-fall",
            "antifall",
            "wialarm",
            "aralarm",
            "inactivity",
        ]
    ):
        return "Home Safety, Presence & Inactivity"
    if any(
        k in text
        for k in [
            "edge",
            "esp32",
            "benchmark",
            "dataset",
            "csi-bench",
            "sensefi",
            "wimans",
            "ehunam",
            "data leakage",
            "efficientfi",
            "babymamba",
            "802.11bf",
        ]
    ):
        return "Edge Systems & Benchmark Rigor"
    return "General WiFi Sensing"


def main():
    pdf_files = sorted(glob.glob("data/raw_papers/*.pdf"))
    print(f"[*] Processing {len(pdf_files)} PDFs in data/raw_papers/...")

    corpus = []
    category_counts = {}

    for fpath in pdf_files:
        fname = os.path.basename(fpath)
        serial = None
        m = re.match(r"^(\d+)_", fname)
        if m:
            serial = int(m.group(1))

        core_info = extract_pdf_core(fpath)
        exp = EXPANDED_DATA.get(serial, {})

        cat = categorize_paper(
            fname, core_info["title"], core_info["abstract"], exp
        )
        category_counts[cat] = category_counts.get(cat, 0) + 1

        entry = {
            "filename": fname,
            "serial": serial,
            "title": core_info["title"],
            "pages": core_info["pages"],
            "category": cat,
            "abstract": core_info["abstract"],
            "conclusion": core_info["conclusion"],
            "expanded_notes": exp,
        }
        corpus.append(entry)

    out_json = REPO_ROOT / "data" / "corpus_summary.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"[+] Wrote {len(corpus)} entries to {out_json.relative_to(REPO_ROOT)}")
    print("[*] Category Breakdown:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"    - {cat}: {count} papers")


if __name__ == "__main__":
    main()
