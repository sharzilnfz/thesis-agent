#!/usr/bin/env python3
"""
Automated downloader for open-access papers into data/raw_papers/.
Supports:
- arXiv preprints (https://arxiv.org/pdf/<id>.pdf)
- Direct PDF URLs (cswu.me, eng.auburn.edu, hal.science)
- MDPI open-access papers
- Updates pdf_path in data/papers.json

Implements principle-build-the-lever and principle-prove-it-works.
"""
import json
import re
import time
from pathlib import Path
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
PAPERS_PATH = REPO_ROOT / "data" / "papers.json"
RAW_PAPERS_DIR = REPO_ROOT / "data" / "raw_papers"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_pdf_download_url(paper: dict) -> str:
    url = paper.get("metadata", {}).get("source_url", "")
    arxiv_id = paper.get("arxiv_id", "")

    # Direct PDF links
    if url.endswith(".pdf"):
        return url

    # arXiv links
    if arxiv_id:
        clean_id = arxiv_id.replace("arxiv:", "")
        return f"https://arxiv.org/pdf/{clean_id}.pdf"

    if "arxiv.org" in url:
        m = re.search(r"arxiv\.org/(?:abs|html)/([0-9]+\.[0-9]+)", url)
        if m:
            return f"https://arxiv.org/pdf/{m.group(1)}.pdf"

    # MDPI open access links
    if "mdpi.com" in url:
        return f"{url.rstrip('/')}/pdf"

    return ""


def main():
    RAW_PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    if not PAPERS_PATH.exists():
        print("[-] data/papers.json not found.")
        return

    with open(PAPERS_PATH, "r", encoding="utf-8") as f:
        papers = json.load(f)

    headers = {"User-Agent": USER_AGENT}
    success_count = 0
    skipped_count = 0

    for pid, p in papers.items():
        bib_key = p.get("bibtex_key", "paper")
        dest_pdf = RAW_PAPERS_DIR / f"{bib_key}.pdf"

        # Check if already present
        if dest_pdf.exists() and dest_pdf.stat().st_size > 10000:
            p["pdf_path"] = str(dest_pdf.relative_to(REPO_ROOT))
            skipped_count += 1
            continue

        dl_url = get_pdf_download_url(p)
        if not dl_url:
            continue

        print(f"[*] Downloading {bib_key} from {dl_url}...")
        try:
            time.sleep(1.0)
            resp = requests.get(dl_url, headers=headers, timeout=25, allow_redirects=True)
            if resp.status_code == 200 and len(resp.content) > 10000 and resp.content.startswith(b"%PDF"):
                with open(dest_pdf, "wb") as f_out:
                    f_out.write(resp.content)
                p["pdf_path"] = str(dest_pdf.relative_to(REPO_ROOT))
                print(f"    [+] Saved {dest_pdf.name} ({len(resp.content) // 1024} KB)")
                success_count += 1
            else:
                print(f"    [-] Skipped {bib_key}: status {resp.status_code}, length {len(resp.content)}")
        except Exception as e:
            print(f"    [-] Failed downloading {bib_key}: {e}")

    with open(PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Summary: {success_count} downloaded, {skipped_count} existing, {len(papers)} total in corpus.")


if __name__ == "__main__":
    main()
