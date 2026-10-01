#!/usr/bin/env python3
"""
Lightweight passage quote extractor using PyMuPDF.
Given a local PDF and a search string/regex, locates the exact page and surrounding context.
Usage:
    python scripts/extract_passages.py --pdf storage/pdfs/sample.pdf --query "relying entirely on an attention"
"""
import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("[-] PyMuPDF not installed. Install with `pip install PyMuPDF` to enable automated PDF quote extraction.")
    sys.exit(0)

def extract_passage(pdf_path: str, query: str, context_chars: int = 250):
    p = Path(pdf_path)
    if not p.exists():
        print(f"[-] Error: File not found: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    found = False
    query_lower = query.lower()

    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text("text")
        lower_text = text.lower()
        idx = lower_text.find(query_lower)
        
        if idx != -1:
            start = max(0, idx - 50)
            end = min(len(text), idx + len(query) + context_chars)
            passage = " ".join(text[start:end].split())
            print(f"[+] Found match on Page {page_idx + 1}:")
            print(f"    \"{passage}\"\n")
            found = True

    if not found:
        print(f"[-] No matching passage found for '{query}' in {pdf_path}")

def main():
    parser = argparse.ArgumentParser(description="Extract passage and page number from local PDF.")
    parser.add_argument("--pdf", required=True, help="Path to PDF")
    parser.add_argument("--query", required=True, help="Substring or phrase to locate")
    args = parser.parse_args()
    extract_passage(args.pdf, args.query)

if __name__ == "__main__":
    main()
