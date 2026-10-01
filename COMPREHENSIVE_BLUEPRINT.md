# ThesisAgent: Steerable Research Workspace for Claude Code, OpenCode & Hermes
## Product Blueprint & Practical Implementation Guide (File-First Architecture)

---

## 1. Executive Summary & Design Pivot

This document is the revised, file-first specification for **ThesisAgent**. It strips away beginner-hostile infrastructure (Docker, heavy Java GROBID, self-managed PostgreSQL clusters, and bespoke Python bot servers) in favor of a **native agentic research workspace**.

### The Core Premise
You already use **Claude Code**, **OpenCode**, and **Hermes Agent** connected to a **CLI API Proxy** (`CLIProxyAPI`, `llm-cli-proxy`, or `commons-proxy`). The workspace leverages these tools directly via the **Agent Skills open standard** (`.claude/skills/` and `.claude/agents/`).

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ REMOVED (Zero Infra Overhead)         │ KEPT (High-Value Research Logic)      │
├───────────────────────────────────────┼──────────────────────────────────────┤
│ ❌ Docker & container networking      │ ✅ Evidence Ledger First             │
│ ❌ PostgreSQL / pgvector management   │ ✅ 4 Human Steering Gates            │
│ ❌ Java GROBID server (~2GB RAM)      │ ✅ Scholarly APIs (arXiv/S2/OpenAlex)│
│ ❌ Heavy PaSa 7B RL crawler weights   │ ✅ Adversarial Falsification Loops   │
│ ❌ Custom LangGraph + Telegram daemon │ ✅ CLI API Proxy Integration         │
│ ❌ Mandatory Karpathy ML training loop│ ✅ `program.md` Human Research Agenda│
└───────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Competitive Landscape & Reference Tools

| Tool | Category | Takeaway for ThesisAgent | Link |
| :--- | :--- | :--- | :--- |
| **`karpathy/autoresearch`** | Research Loop | Adopt **`program.md`** as your human-maintained research agenda. Keep code experimentation as an optional module if your thesis has code. | [GitHub](https://github.com/karpathy/autoresearch) |
| **`Future-House/paper-qa`** | Evidence Verification | Optional secondary CLI checker (`pqa ask`) for contradiction checks. Do not make it mandatory on Day 1. | [GitHub](https://github.com/Future-House/paper-qa) |
| **`bytedance/pasa`** | Citation Navigation | Copy the **pattern** (keyword $\to$ abstract scan $\to$ 1-hop forward/backward citation expansion $\to$ LLM selection) in lightweight Python. | [GitHub](https://github.com/bytedance/pasa) |
| **`HadiFrt20/deepresearch`** | Adversarial Verification | Borrow the **sidecar adversary pattern** (`.adversary.json`): formulate counter-queries to search for refutations. | [GitHub](https://github.com/HadiFrt20/deepresearch) |
| **`aiming-lab/AutoResearchClaw`** | Multi-Agent Review | Multi-perspective simulated peer review before merging drafts. | [GitHub](https://github.com/aiming-lab/AutoResearchClaw) |
| **`NousResearch/hermes-agent`** | Long-Horizon Agent | Use Hermes strictly as an external cron scheduler for weekly arXiv/Semantic Scholar delta sweeps. | [GitHub](https://github.com/NousResearch/hermes-agent) |
| **`router-for-me/CLIProxyAPI`** | LLM Gateway | Standard OpenAI-compatible base URL (`http://localhost:8317/v1`) routing Claude/Gemini/Codex subscriptions. | [GitHub](https://github.com/router-for-me/CLIProxyAPI) |

---

## 3. The File-First System Architecture

```
                               ┌────────────────────────────────┐
                               │     Researcher (You)           │
                               │  Terminal (Claude/OpenCode)    │
                               └───────────────┬────────────────┘
                                               │
                                 Slash Commands / Prompts
                                               │
                                               ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ AGENT HARNESS (Claude Code / OpenCode)                                                   │
 │ - Powered by your CLI API Proxy (`http://localhost:8317/v1`)                            │
 │ - Governed by `CLAUDE.md` and your evolving `program.md` agenda                          │
 │ - Orchestrates subagents and enforces the 4 Human Steering Gates                         │
 └──────────────┬──────────────────────────────┬───────────────────────────────┬────────────┘
                │                              │                               │
         Calls Subagents                Executes Scripts                Directs Review
                ▼                              ▼                               ▼
 ┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌──────────────────────────┐
 │ Specialized Agents          │ │ Deterministic Tools         │ │ Flat Epistemic State     │
 │                             │ │                             │ │                          │
 │ • @scout (Citation Search)  │ │ • `scripts/scholar_search`  │ │ • `data/papers.json`     │
 │ • @adversary (Falsification)│ │ • `scripts/extract_passage` │ │ • `data/evidence_ledger` │
 │ • @writer (LaTeX Synthesis) │ │ • `scripts/verify_bibtex`   │ │ • `paper/references.bib` │
 │ • @auditor (Gatekeeper)     │ │ • `scripts/arxiv_monitor`   │ │ • `paper/chapters/*.tex` │
 └─────────────────────────────┘ └─────────────────────────────┘ └──────────────────────────┘
```

---

## 4. The 4 Human Steering Gates

The agent must pause at explicit checkpoints before spending tokens or modifying drafts:

```
[Topic in program.md]
         │
         ▼
 ┌───────────────┐
 │ GATE 1: SCOPE │ ──> Human approves query taxonomy, inclusion/exclusion rules, and key venues.
 └───────┬───────┘
         │
         ▼
 [Harvest & Screening via scholar_search.py]
         │
         ▼
 ┌────────────────┐
 │ GATE 2: CORPUS │ ──> Human reviews included vs. excluded papers in `data/papers.json`.
 └───────┬────────┘
         │
         ▼
 [Passage Extraction & Adversary Falsification]
         │
         ▼
 ┌──────────────┐
 │ GATE 3: GAPS │ ──> Human reviews conflicting findings, limitations, and chosen thesis angle.
 └───────┬──────┘
         │
         ▼
 [Section Drafting & verify_bibtex.py Check]
         │
         ▼
 ┌───────────────┐
 │ GATE 4: DRAFT │ ──> Human reviews compiled LaTeX diff and verified citation proofs.
 └───────────────┘
```

---

## 5. File System Layout

The complete project structure to be initialized in `Projects/thesis-agent/`:

```text
thesis-agent/
├── CLAUDE.md                    # System instructions, formatting rules, tool execution policies
├── program.md                   # Human-maintained thesis agenda, hypotheses, and milestones
├── .env.example                 # API keys (Semantic Scholar API key, proxy URL)
├── data/
│   ├── papers.json              # Canonical registry of discovered/screened papers (keyed by DOI/arXiv)
│   ├── evidence_ledger.json     # Factual statements mapped to exact quotes, page numbers, and BibTeX keys
│   └── gaps.json                # Identified literature gaps, contradictions, and adversary attack results
├── paper/
│   ├── main.tex                 # Root LaTeX document
│   ├── references.bib           # Verified BibTeX file
│   └── chapters/
│       ├── ch1_intro.tex
│       ├── ch2_lit_review.tex
│       ├── ch3_methodology.tex
│       └── ch4_results.tex
├── storage/
│   └── pdfs/                    # Local storage for downloaded/manual paper PDFs
└── scripts/
    ├── scholar_search.py        # Robust arXiv + Semantic Scholar + OpenAlex search with rate limiting
    ├── extract_passages.py      # Lightweight PyMuPDF passage search and quote extractor
    ├── verify_bibtex.py         # Deterministic gatekeeper: asserts every \cite{} has a verified ledger passage
    └── arxiv_monitor.py         # Weekly delta scanner for Hermes cron
```

---

## 6. Deterministic Scripts & Schemas

### 6.1 `data/papers.json` Schema
Papers are indexed by normalized ID (`doi:10.xxx` or `arxiv:YYMM.NNNNN`) to prevent duplicates:
```json
{
  "arxiv:1706.03762": {
    "id": "arxiv:1706.03762",
    "doi": "10.48550/arxiv.1706.03762",
    "title": "Attention Is All You Need",
    "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
    "year": 2017,
    "venue": "NeurIPS",
    "bibtex_key": "vaswani2017attention",
    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
    "pdf_path": "storage/pdfs/vaswani2017attention.pdf",
    "screening_status": "included",
    "screening_reason": "Foundational Transformer architecture reference"
  }
}
```

### 6.2 `data/evidence_ledger.json` Schema
```json
{
  "ev_001": {
    "evidence_id": "ev_001",
    "paper_id": "arxiv:1706.03762",
    "bibtex_key": "vaswani2017attention",
    "claim": "The Transformer architecture relies entirely on an attention mechanism without recurrence.",
    "exact_passage": "We propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output.",
    "page_number": 2,
    "section": "1 Introduction",
    "stance": "supports",
    "adversary_status": "confirmed"
  }
}
```

---

### 6.3 Scholarly Harvesting Script (`scripts/scholar_search.py`)
*Features exponential backoff, rate limiting, and canonical ID deduplication.*

```python
#!/usr/bin/env python3
"""
Robust scholarly search for arXiv, Semantic Scholar, and OpenAlex.
Usage: python scripts/scholar_search.py --query "sparse autoencoders" --limit 5
"""
import os
import re
import json
import time
import argparse
import requests
from typing import Dict, List

PAPERS_PATH = "data/papers.json"
S2_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")

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

def generate_bibtex_key(author: str, year: int, title: str) -> str:
    first_author = re.sub(r"[^a-zA-Z]", "", author.split()[-1].lower()) if author else "anon"
    first_word = re.sub(r"[^a-zA-Z]", "", title.split()[0].lower()) if title else "paper"
    return f"{first_author}{year}{first_word}"

def load_papers() -> Dict:
    if os.path.exists(PAPERS_PATH):
        with open(PAPERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_papers(papers: Dict):
    os.makedirs(os.path.dirname(PAPERS_PATH), exist_ok=True)
    with open(PAPERS_PATH, "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)

def search_semantic_scholar(query: str, limit: int = 5) -> List[Dict]:
    headers = {"x-api-key": S2_API_KEY} if S2_API_KEY else {}
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,venue,abstract,externalIds"
    }
    
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 429:
                time.sleep(2 ** attempt)
                continue
            if resp.status_code != 200:
                return []
            return resp.json().get("data", [])
        except Exception:
            time.sleep(1)
    return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    papers_db = load_papers()
    s2_results = search_semantic_scholar(args.query, args.limit)
    new_count = 0

    for item in s2_results:
        ext = item.get("externalIds", {})
        doi = normalize_doi(ext.get("DOI"))
        arxiv_id = normalize_arxiv(ext.get("ArXiv"))
        canonical_id = doi or arxiv_id
        
        if not canonical_id or canonical_id in papers_db:
            continue

        authors = [a.get("name", "") for a in item.get("authors", [])]
        year = item.get("year") or 2025
        title = item.get("title", "")
        bib_key = generate_bibtex_key(authors[0] if authors else "unknown", year, title)

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
    print(f"[+] Harvested {new_count} new candidate papers. Database has {len(papers_db)} total.")

if __name__ == "__main__":
    main()
```

---

### 6.4 Deterministic Gatekeeper Script (`scripts/verify_bibtex.py`)
*Validates that every `\cite{key}` in LaTeX exists in `references.bib` AND has verified evidence.*

```python
#!/usr/bin/env python3
"""
Integrity gatekeeper: audits all LaTeX files in paper/chapters/ against
references.bib and data/evidence_ledger.json.
Fails with code 1 if any citation is missing or lacks evidence.
"""
import os
import re
import json
import sys

CHAPTERS_DIR = "paper/chapters"
BIBTEX_PATH = "paper/references.bib"
LEDGER_PATH = "data/evidence_ledger.json"

def extract_tex_citations(chapters_dir: str) -> set:
    citations = set()
    cite_pattern = re.compile(r"\\cite(?:\[.*?\])?\{([^}]+)\}")
    
    if not os.path.exists(chapters_dir):
        return citations

    for fname in os.listdir(chapters_dir):
        if fname.endswith(".tex"):
            with open(os.path.join(chapters_dir, fname), "r", encoding="utf-8") as f:
                for line in f:
                    # Skip commented lines
                    if line.strip().startswith("%"):
                        continue
                    matches = cite_pattern.findall(line)
                    for m in matches:
                        for key in m.split(","):
                            citations.add(key.strip())
    return citations

def load_bibtex_keys(bib_path: str) -> set:
    keys = set()
    if not os.path.exists(bib_path):
        return keys
    key_pattern = re.compile(r"@\w+\s*\{\s*([^,]+),")
    with open(bib_path, "r", encoding="utf-8") as f:
        for line in f:
            match = key_pattern.match(line.strip())
            if match:
                keys.add(match.group(1).strip())
    return keys

def load_ledger_keys(ledger_path: str) -> set:
    if not os.path.exists(ledger_path):
        return set()
    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)
    return {entry.get("bibtex_key") for entry in ledger.values() if entry.get("bibtex_key")}

def main():
    tex_cites = extract_tex_citations(CHAPTERS_DIR)
    bib_keys = load_bibtex_keys(BIBTEX_PATH)
    ledger_keys = load_ledger_keys(LEDGER_PATH)

    print(f"[*] Auditing {len(tex_cites)} citations across {CHAPTERS_DIR}/*.tex...")
    
    missing_in_bib = tex_cites - bib_keys
    missing_in_ledger = tex_cites - ledger_keys

    errors = 0
    if missing_in_bib:
        print(f"[-] ERROR: Citations missing from {BIBTEX_PATH}:")
        for k in missing_in_bib:
            print(f"    - \\cite{{{k}}}")
        errors += 1

    if missing_in_ledger:
        print(f"[-] ERROR: Citations lacking verified passages in {LEDGER_PATH}:")
        for k in missing_in_ledger:
            print(f"    - \\cite{{{k}}}")
        errors += 1

    if errors > 0:
        print(f"[-] AUDIT FAILED with {errors} violations. Draft cannot be finalized.")
        sys.exit(1)

    print("[+] AUDIT PASSED: All citations are present in .bib and grounded in the Evidence Ledger.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 7. Master Configuration (`CLAUDE.md`)

Place this file at the repository root. Both Claude Code and OpenCode read it on startup:

```markdown
# ThesisAgent: Operational Protocol

## 1. Project Context
- **Role:** Autonomous Academic Research Assistant for an Undergraduate Thesis.
- **Tone:** Academic, rigorous, skeptical, and formal.
- **Language Stack:** Python 3.10+, LaTeX (pdflatex / latexmk), BibLaTeX.

## 2. Model Routing via CLI Proxy
All subagents must operate through the running CLI API Proxy endpoint:
- **Base URL:** `http://localhost:8317/v1` (or local env `CLI_PROXY_BASE_URL`)
- **API Key:** `cli-proxy-token`
- **Model Aliases:**
  - `gemini-2.0-flash`: Broad search, filtering, and JSON extraction.
  - `claude-3-5-sonnet`: Academic prose writing and LaTeX synthesis.
  - `deepseek-r1` or `claude-3-7-sonnet`: Adversarial counter-queries and logic auditing.

## 3. Strict Academic Rules
1. **Zero Hallucinated Citations:** Never emit a `\cite{key}` unless the key exists in `paper/references.bib` AND is present in `data/evidence_ledger.json`.
2. **The 4 Human Gates:**
   - Never initiate broad harvesting before the user approves Gate 1 (Scope).
   - Never extract text from unapproved papers before Gate 2 (Corpus).
   - Never draft sections before resolving Gate 3 (Gaps).
   - Never merge text before passing `python scripts/verify_bibtex.py` (Gate 4).
3. **Purity of Tone:** No filler, no sycophantic praise, no narrating comments in code.

## 4. Subagent Definitions
- `@scout`: Runs `scripts/scholar_search.py` and populates `data/papers.json`.
- `@adversary`: Takes claims and searches for counter-evidence, generating `data/gaps.json`.
- `@writer`: Drafts LaTeX files in `paper/chapters/` following academic structure.
- `@auditor`: Runs `python scripts/verify_bibtex.py` and audits sentence entailment.
```

---

## 8. Action Order & Practical Implementation Steps

Follow this order to get the system operational:

1. **Step 1: Workspace Setup**
   - In `Projects/thesis-agent/`, ensure the directory tree exists: `data/`, `paper/chapters/`, `storage/pdfs/`, `scripts/`.
   - Add `CLAUDE.md` and `program.md`.
2. **Step 2: Add Scripts**
   - Save `scripts/scholar_search.py` and `scripts/verify_bibtex.py`.
   - Run a quick test: `python scripts/scholar_search.py --query "sparse autoencoders" --limit 3` to verify that `data/papers.json` is generated.
3. **Step 3: Define Agent Prompts**
   - Create `.claude/agents/scout.md`, `adversary.md`, `writer.md`, and `auditor.md`.
   - Create slash commands in `.claude/skills/` (`/lit-review`, `/find-gaps`, `/draft-tex`).
4. **Step 4: Launch CLI Proxy**
   - Start your proxy server (e.g., `CLIProxyAPI` on port 8317).
   - Open terminal in `Projects/thesis-agent/` and launch `claude` or `opencode`.
5. **Step 5: Execute First Controlled Loop**
   - Type `/lit-review "your thesis topic"`.
   - Steer through Gate 1 (Scope) and Gate 2 (Corpus).
   - Run `/draft-tex 2` and verify that the gatekeeper script passes before writing to `ch2_lit_review.tex`.
6. **Step 6: Hermes Cron (Optional Final Addition)**
   - Configure a weekly Hermes cron task to run `scripts/arxiv_monitor.py` and notify you of newly published preprints on Telegram.
