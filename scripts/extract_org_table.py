#!/usr/bin/env python3
"""Extract logic vocabulary org-table from Denote source into normalized JSON.

Source: ~/sync/org/notes/20230617T120300--용어-말꼴-배움낱말-테이블__dictionary_glossary_logic_orgtable.org

Output: raw.json — one entry per source row, with parsed fields and audit info.
This is intermediate data. core.yaml is hand-curated on top of this.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SOURCE = Path.home() / "sync/org/notes/20230617T120300--용어-말꼴-배움낱말-테이블__dictionary_glossary_logic_orgtable.org"

TYPO_FIXES = {
    "weak inferes": "weak inference",
    "quantificationa logic": "quantificational logic",
    "걸론": "결론",
    "귀걸": "귀결",
    "DeMorgan' rule of disjunction": "De Morgan's rule of disjunction",
    "DeMorgan' rule of conjunction": "De Morgan's rule of conjunction",
    "proposition ‘statement": "proposition / statement",
    "assumption ‘supposition": "assumption / supposition",
    "cogent- persuasive inference": "cogent / persuasive inference",
}


def parse_table(text: str) -> list[dict]:
    """Parse the org-table after the '언어 테이블 영어' heading."""
    rows = []
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if not in_table:
            if stripped.startswith("|") and "영어" in stripped and "한자말" in stripped:
                in_table = True
            continue
        if not stripped.startswith("|"):
            if rows:
                break
            continue
        if stripped.startswith("|-"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 3:
            continue
        en, hanja, hanmal = cells[0], cells[1], cells[2]
        if en == "영어":
            continue
        rows.append({"en_raw": en, "hanja_raw": hanja, "hanmal_raw": hanmal})
    return rows


def fix_typos(s: str) -> tuple[str, bool]:
    for bad, good in TYPO_FIXES.items():
        if bad in s:
            return s.replace(bad, good), True
    return s, False


def split_alternates(s: str) -> list[str]:
    """Split on ㆍ or '/' to expand alternates."""
    parts = re.split(r"[ㆍ／]", s)
    return [p.strip() for p in parts if p.strip()]


def main() -> int:
    if not SOURCE.exists():
        print(f"source not found: {SOURCE}", file=sys.stderr)
        return 1

    text = SOURCE.read_text(encoding="utf-8")
    raw_rows = parse_table(text)

    entries = []
    for idx, row in enumerate(raw_rows, start=1):
        en_fixed, en_typo = fix_typos(row["en_raw"])
        hanja_fixed, hanja_typo = fix_typos(row["hanja_raw"])
        entries.append({
            "row": idx,
            "en_raw": row["en_raw"],
            "hanja_raw": row["hanja_raw"],
            "hanmal_raw": row["hanmal_raw"],
            "en": en_fixed,
            "hanja_alternates": split_alternates(hanja_fixed),
            "hanmal_alternates": split_alternates(row["hanmal_raw"]),
            "typo_fixed": en_typo or hanja_typo,
        })

    # detect duplicates by (en, hanja first alternate)
    seen = {}
    for e in entries:
        key = (e["en"].lower(), e["hanja_alternates"][0].lower() if e["hanja_alternates"] else "")
        seen.setdefault(key, []).append(e["row"])
    duplicates = {k: v for k, v in seen.items() if len(v) > 1}

    output = {
        "source_id": "20230617T120300",
        "source_path": str(SOURCE),
        "row_count": len(entries),
        "duplicate_groups": [{"key": list(k), "rows": v} for k, v in duplicates.items()],
        "entries": entries,
    }
    out_path = SOURCE.parent.parent  # ignored
    out_path = Path(__file__).resolve().parent.parent / "vocab" / "raw.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out_path} ({len(entries)} entries, {len(duplicates)} duplicate keys)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
