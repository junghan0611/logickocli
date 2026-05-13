#!/usr/bin/env python3
"""Vocab self-check — counts, alias collisions, schema sanity, test wiring.

Usage:
    python3 scripts/check_vocab.py            # full report
    python3 scripts/check_vocab.py --quiet    # only failures
    python3 scripts/check_vocab.py --json     # machine output

Exit code 0 if no unexpected issues, 1 otherwise.

This is Phase 1 — no CLI binary yet. The Phase 2 CLI will import the same
checks.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "vocab"
TESTS = ROOT / "tests"

# Alias collisions that are intended by design.
# See vocab/SCHEMA.md § Alias 충돌.
INTENDED_COLLISIONS: set[frozenset[str]] = {
    frozenset({"PROP.CONDITIONAL", "SEM.CONDITIONAL_SENTENCE"}),
    frozenset({"PROP.BICONDITIONAL", "SEM.BICONDITIONAL_SENTENCE"}),
    frozenset({"PROP.BICONDITIONAL", "META.LOGICAL_EQUIVALENCE"}),
    frozenset({"META.PREMISE", "META.ASSUMPTION"}),
}


def as_list(v):
    if v is None:
        return []
    return [v] if isinstance(v, str) else list(v)


def load_vocab() -> tuple[list[dict], list[dict]]:
    core = yaml.safe_load((VOCAB / "core.yaml").read_text(encoding="utf-8"))
    fall = yaml.safe_load((VOCAB / "fallacies.yaml").read_text(encoding="utf-8"))
    return core["entries"], fall["entries"]


def count_entries(core, fall):
    return {
        "core": len(core),
        "fallacies": len(fall),
        "total_unique_ids": len({e["id"] for e in core + fall}),
        "domain_breakdown": dict(Counter(e.get("domain", "?") for e in core)),
        "fallacy_breakdown": dict(
            Counter(f"{e['kind']}/{e.get('subtype', '-')}" for e in fall)
        ),
    }


def find_duplicate_ids(core, fall):
    all_ids = [e["id"] for e in core + fall]
    return [k for k, v in Counter(all_ids).items() if v > 1]


def find_alias_collisions(core, fall):
    """Same surface string mapping to multiple distinct IDs.

    Surface is field-agnostic: a user typing '단순조건문' should match
    regardless of whether it lives in canonical_ko or aliases_ko of some
    entry. We track which fields the surface appeared in for debugging.
    """
    surface: dict[str, dict] = {}
    for e in core + fall:
        eid = e["id"]
        for field, vals in (
            ("canonical_ko", as_list(e.get("canonical_ko"))),
            ("aliases_ko", as_list(e.get("aliases_ko"))),
            ("native_aliases", as_list(e.get("native_aliases"))),
            ("symbol", as_list(e.get("symbol"))),
            ("en", [en.lower() for en in as_list(e.get("en"))]),
        ):
            for v in vals:
                rec = surface.setdefault(v, {"ids": [], "fields": set()})
                if eid not in rec["ids"]:
                    rec["ids"].append(eid)
                rec["fields"].add(field)

    collisions = []
    for val, rec in surface.items():
        if len(rec["ids"]) > 1:
            collisions.append({
                "value": val,
                "ids": rec["ids"],
                "fields": sorted(rec["fields"]),
            })
    return collisions


def classify_collisions(collisions):
    intended, unexpected = [], []
    for c in collisions:
        key = frozenset(c["ids"])
        # if collision is a subset of an intended set, treat as intended
        bucket = intended if any(key <= s for s in INTENDED_COLLISIONS) else unexpected
        bucket.append(c)
    return intended, unexpected


def check_schema(core, fall):
    """Light schema check — required fields, type sanity."""
    issues = []
    required_core = {"id", "domain", "kind", "canonical_ko"}
    required_fall = {"id", "kind", "canonical_ko"}
    for e in core:
        missing = required_core - e.keys()
        if missing:
            issues.append({"id": e.get("id", "?"), "missing": sorted(missing)})
    for e in fall:
        missing = required_fall - e.keys()
        if missing:
            issues.append({"id": e.get("id", "?"), "missing": sorted(missing)})
    return issues


def check_test_wiring(core, fall):
    """Every expect_id in tests/normalization.yaml must resolve to an existing entry."""
    norm = yaml.safe_load((TESTS / "normalization.yaml").read_text(encoding="utf-8"))
    valid_ids = {e["id"] for e in core + fall}
    dangling = []
    for case in norm["cases"]:
        ids = []
        if "expect_id" in case:
            ids = [case["expect_id"]]
        elif "expect_id_any_of" in case:
            ids = case["expect_id_any_of"]
        for i in ids:
            if i not in valid_ids:
                dangling.append({"case_inputs": case.get("inputs", [])[:1], "id": i})
    return dangling


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    core, fall = load_vocab()
    report = {
        "counts": count_entries(core, fall),
        "duplicate_ids": find_duplicate_ids(core, fall),
        "schema_issues": check_schema(core, fall),
        "dangling_test_ids": check_test_wiring(core, fall),
    }
    intended, unexpected = classify_collisions(find_alias_collisions(core, fall))
    report["intended_collisions"] = intended
    report["unexpected_collisions"] = unexpected

    failed = bool(
        report["duplicate_ids"]
        or report["schema_issues"]
        or report["dangling_test_ids"]
        or report["unexpected_collisions"]
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if failed else 0

    c = report["counts"]
    if not args.quiet:
        print(f"entries: core={c['core']}, fallacies={c['fallacies']}, "
              f"total unique IDs={c['total_unique_ids']}")
        print("\ncore domains:")
        for d, n in sorted(c["domain_breakdown"].items(), key=lambda x: -x[1]):
            print(f"  {d:24s} {n}")
        print("\nfallacy kinds:")
        for k, n in c["fallacy_breakdown"].items():
            print(f"  {k:24s} {n}")
        print(f"\nintended alias collisions: {len(intended)}")
        for col in intended:
            print(f"  {col['value']!r}  →  {col['ids']}  (fields: {col['fields']})")

    if report["duplicate_ids"]:
        print(f"\nFAIL duplicate IDs: {report['duplicate_ids']}")
    if report["schema_issues"]:
        print(f"\nFAIL schema issues: {len(report['schema_issues'])}")
        for s in report["schema_issues"]:
            print(f"  {s['id']}: missing {s['missing']}")
    if report["dangling_test_ids"]:
        print(f"\nFAIL dangling test IDs: {len(report['dangling_test_ids'])}")
        for d in report["dangling_test_ids"]:
            print(f"  {d['id']}  (case: {d['case_inputs']})")
    if unexpected:
        print(f"\nFAIL unexpected alias collisions: {len(unexpected)}")
        for col in unexpected:
            print(f"  {col['value']!r}  →  {col['ids']}  (fields: {col['fields']})")

    if not failed and not args.quiet:
        print("\nOK — no unexpected issues.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
