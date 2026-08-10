"""Batch support/Laurent verification for a fixed killer-union skeleton."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from certify_union_orbit_supports import certify_orbit
from enumerate_killer_union_orbits import parse_edges, union_from_missing


def verify_item(
    item: tuple[int, list[list[int]], set[tuple[int, int]], int]
) -> dict[str, object]:
    orbit_index, pattern, union_edges, max_certificates = item
    result = certify_orbit(pattern, union_edges, max_certificates)
    return {
        "orbit": orbit_index,
        "status": result["status"],
        "variables": result["variables"],
        "certificate_count": len(result["certificates"]),
        "survivor_support": result.get("support_nonzero"),
        "survivor_metadata": result.get("metadata"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--missing-edges", required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--max-certificates", type=int, default=10_000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.orbits.read_text(encoding="utf-8"))
    patterns = payload["representatives"]
    if args.limit is not None:
        patterns = patterns[: args.limit]
    union_edges = set(
        union_from_missing(parse_edges(args.missing_edges))
    )
    items = [
        (index, pattern, union_edges, args.max_certificates)
        for index, pattern in enumerate(patterns)
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(verify_item, items))
    else:
        rows = [verify_item(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    failures = [
        row
        for row in rows
        if row["status"]
        not in {
            "certified",
            "unconditional_laurent_contradiction",
        }
    ]
    result = {
        "orbits_checked": len(rows),
        "status_counts": dict(counts),
        "total_laurent_conflict_cubes": sum(
            int(row["certificate_count"]) for row in rows
        ),
        "minimum_conflict_cubes": min(
            int(row["certificate_count"]) for row in rows
        ),
        "maximum_conflict_cubes": max(
            int(row["certificate_count"]) for row in rows
        ),
        "failures": failures,
        "rows": rows,
    }
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: checked={len(rows)} "
            f"counts={dict(counts)}"
        )
    else:
        print(text)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
