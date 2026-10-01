#!/usr/bin/env python3
"""
Robust scholarly harvesting tool for Semantic Scholar, arXiv, and OpenAlex.
Features:
- Absolute repo-root path resolution
- User-Agent header + 1-second polite rate-limiting
- Fallback corpus ID when DOI/arXiv ID are missing
- Deduplication and BibTeX key collision avoidance
"""
import os
import re
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List
import requests
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_PATH = REPO_ROOT / "data" / "papers.json"
S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
USER_AGENT = "ThesisAgent/1.0 (academic research bot; mailto:contact@localhost)"

def normalize_doi(doi: str) -> str:
    if not doi:
        return ""
    clean = doi.strip().lower()
    clean = re.sub(r"^https?://(dx\.)?doi\.org/", "", clean)
    return f"doi:{clean}"

def normalize_arxiv(arxiv_id: str) -> str:
    if not arxiv_id:
        return ""
    clean = arxiv_id.strip().lower()
    clean = re.sub(r"^arxiv:", "", clean)
    clean = re.sub(r"v\d+$", "", clean)
    return f"arxiv:{clean}"

def generate_bibtex_key(author: str, year: int, title: str, existing_keys: set) -> str:
    first_author = re.sub(r"[^a-zA-Z]", "", author.split()[-1].lower()) if author else "anon"
    words = [re.sub(r"[^a-zA-Z]", "", w.lower()) for w in title.split() if w]
    first_word = words[0] if words else "paper"
    base_key = f"{first_author}{year}{first_word}"
    
    candidate_key = base_key
    suffix_char = ord('b')
    while candidate_key in existing_keys:
        candidate_key = f"{base_key}{chr(suffix_char)}"
        suffix_char += 1
    existing_keys.add(candidate_key)
    return candidate_key

def load_papers() -> Dict:
    if PAPERS_PATH.exists():
        try:
            with open(PAPERS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_papers(papers: Dict):
    PAPERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

def search_semantic_scholar(query: str, limit: int = 5) -> List[Dict]:
    headers = {"User-Agent": USER_AGENT}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,venue,abstract,externalIds,paperId"
    }
    for attempt in range(3):
        try:
            time.sleep(1.0)  # Polite throttle
            resp = requests.get(url, params=params, headers=headers, timeout=12)
            if resp.status_code == 429:
                time.sleep(2 ** attempt + 1)
                continue
            if resp.status_code != 200:
                return []
            return resp.json().get("data", [])
        except Exception:
            time.sleep(1)
    return []

def search_arxiv_fallback(query: str, limit: int = 5) -> List[Dict]:
    """Fallback search over arXiv Atom feed."""
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit
    }
    try:
        time.sleep(1.0)
        resp = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=12)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.content)
        entries = []
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            id_url = entry.find("atom:id", ns).text
            arxiv_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else id_url
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            published = entry.find("atom:published", ns).text[:4]
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            entries.append({
                "paperId": f"arxiv_{arxiv_id}",
                "title": title,
                "authors": [{"name": n} for n in authors],
                "year": int(published) if published.isdigit() else 2025,
                "venue": "arXiv",
                "abstract": summary,
                "externalIds": {"ArXiv": arxiv_id}
            })
        return entries
    except Exception:
        return []

def main():
    parser = argparse.ArgumentParser(description="Harvest academic papers from scholarly APIs.")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument("--limit", type=int, default=5, help="Number of papers to fetch")
    args = parser.parse_args()

    papers_db = load_papers()
    existing_bib_keys = {p.get("bibtex_key") for p in papers_db.values() if p.get("bibtex_key")}

    # Step 1: Semantic Scholar search
    results = search_semantic_scholar(args.query, args.limit)
    
    # Step 2: Fallback to arXiv if S2 yields zero
    if not results:
        results = search_arxiv_fallback(args.query, args.limit)

    new_count = 0
    for item in results:
        ext = item.get("externalIds", {}) or {}
        doi = normalize_doi(ext.get("DOI"))
        arxiv_id = normalize_arxiv(ext.get("ArXiv"))
        paper_id = item.get("paperId", "")
        
        # Primary canonical ID, fallback to S2 paperId instead of silent drop
        canonical_id = doi or arxiv_id or (f"s2:{paper_id}" if paper_id else None)
        if not canonical_id or canonical_id in papers_db:
            continue

        authors = [a.get("name", "") for a in item.get("authors", [])]
        year = item.get("year") or 2025
        title = item.get("title", "Untitled")
        bib_key = generate_bibtex_key(authors[0] if authors else "unknown", year, title, existing_bib_keys)

        papers_db[canonical_id] = {
            "id": canonical_id,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "year": year,
            "venue": item.get("venue", ""),
            "bibtex_key": bib_key,
            "abstract": item.get("abstract", ""),
            "pdf_path": None,
            "screening_status": "candidate",
            "screening_reason": f"Discovered via query: '{args.query}'"
        }
        new_count += 1

    save_papers(papers_db)
    print(f"[+] Harvested {new_count} new candidate papers. Database has {len(papers_db)} total records.")

if __name__ == "__main__":
    main()
