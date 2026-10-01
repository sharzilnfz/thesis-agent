#!/usr/bin/env python3
"""
Populate deterministic gap IDs, resolution statuses, and evidence cross-references in data/gaps.json.
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAPS_PATH = REPO_ROOT / "data" / "gaps.json"

LINKED_KEYS = {
    1: ["sok2024sok", "author2020on"],
    2: ["author2025a"],
    3: ["author2022caution"],
    4: ["author2026vitalcsi"],
    5: ["author2019farsense"],
    6: ["author2024mitigating"],
    7: ["author2025a"],
    8: ["author2019zeroeffort"],
    9: ["author2019farsense"],
    10: ["hernandez2024wifi"],
    11: ["author2019widetect"],
    12: ["csi2025csi"],
    13: ["author2026vitalcsi"],
    14: ["csi2025csi"],
    15: ["author2024airfi"],
    16: ["author2019zeroeffort"],
    17: ["author2022caution", "author2024airfi"],
    18: ["hernandez2024wifi", "author2022efficientfi"]
}

def main():
    with open(GAPS_PATH, "r", encoding="utf-8") as f:
        gaps = json.load(f)

    for i, g in enumerate(gaps, start=1):
        g["gap_id"] = f"GAP-{i:02d}"
        g["status"] = "addressed_in_framework"
        g["cross_referenced_bib_keys"] = LINKED_KEYS.get(i, [])

    with open(GAPS_PATH, "w", encoding="utf-8") as f:
        json.dump(gaps, f, indent=2)

    print(f"[+] Updated {len(gaps)} entries in {GAPS_PATH.relative_to(REPO_ROOT)} with valid gap_id and cross-references.")

if __name__ == "__main__":
    main()
