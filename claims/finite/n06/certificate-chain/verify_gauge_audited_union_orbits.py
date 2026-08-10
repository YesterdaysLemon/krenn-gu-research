"""Certify fixed-union orbits with an explicit mutual-weight gauge audit."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from certify_global_pattern_orbits import certify_pattern_with_fallback
from enumerate_killer_union_orbits import parse_edges, union_from_missing
from killer_union_stratum import mutual_gauge_rank
from krenn_gu.search_witness import EquationSystem


def certify_item(
    item: tuple[int, list[list[int]], int, str, str, bool],
) -> dict[str, object]:
    (
        orbit,
        pattern,
        max_certificates,
        fallback_directory,
        support_solver,
        normalize_mutual,
    ) = item
    mutual_edges, gauge_rank = mutual_gauge_rank(
        EquationSystem(6, 3),
        pattern,
    )
    if normalize_mutual and gauge_rank != mutual_edges:
        raise AssertionError("attempted an unjustified normalization")
    result = certify_pattern_with_fallback(
        orbit,
        pattern,
        max_certificates,
        Path(fallback_directory),
        support_solver,
        normalize_mutual=normalize_mutual,
    )
    return {
        "orbit": orbit,
        "pattern": pattern,
        "mutual_edges": mutual_edges,
        "gauge_rank": gauge_rank,
        "normalized": normalize_mutual,
        "status": result["status"],
        "variables": result["variables"],
        "certificates": result["certificates"],
        "exact_certificates": result["exact_certificates"],
        "survivor_support": result.get("support_nonzero"),
        "survivor_metadata": result.get("metadata"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--missing-edges", required=True)
    parser.add_argument(
        "--selection",
        choices=("all", "gauge-full", "gauge-deficient"),
        default="all",
    )
    parser.add_argument("--unnormalized", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--max-certificates", type=int, default=10_000)
    parser.add_argument(
        "--support-solver",
        choices=("cadical195", "glucose42", "minisat22"),
        default="cadical195",
    )
    parser.add_argument("--fallback-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.orbits.read_text(encoding="utf-8"))
    system = EquationSystem(6, 3)
    selected = []
    for orbit, pattern in enumerate(payload["representatives"]):
        mutual_edges, gauge_rank = mutual_gauge_rank(system, pattern)
        if (
            args.selection == "gauge-full"
            and gauge_rank != mutual_edges
        ):
            continue
        if (
            args.selection == "gauge-deficient"
            and gauge_rank == mutual_edges
        ):
            continue
        selected.append((orbit, pattern))
    if args.limit is not None:
        selected = selected[: args.limit]

    expected_union = set(
        union_from_missing(parse_edges(args.missing_edges))
    )
    for _, pattern in selected:
        observed_union = {
            tuple(sorted((vertex, neighbour)))
            for vertex, row in enumerate(pattern)
            for neighbour in row
        }
        if observed_union != expected_union:
            raise AssertionError("pattern union does not match requested case")

    normalize_mutual = not args.unnormalized
    items = [
        (
            orbit,
            pattern,
            args.max_certificates,
            str(args.fallback_directory),
            args.support_solver,
            normalize_mutual,
        )
        for orbit, pattern in selected
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(certify_item, items))
    else:
        rows = [certify_item(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    accepted = {
        "certified",
        "certified_with_exact_fallback",
        "unconditional_laurent_contradiction",
    }
    failures = [
        {
            "orbit": row["orbit"],
            "status": row["status"],
            "survivor_support": row["survivor_support"],
            "survivor_metadata": row["survivor_metadata"],
        }
        for row in rows
        if row["status"] not in accepted
    ]
    result = {
        "orbits_file": str(args.orbits),
        "missing_edges": args.missing_edges,
        "selection": args.selection,
        "normalized": normalize_mutual,
        "orbits_checked": len(rows),
        "status_counts": dict(counts),
        "laurent_certificates": sum(
            len(row["certificates"]) for row in rows
        ),
        "exact_certificates": sum(
            len(row["exact_certificates"]) for row in rows
        ),
        "failures": failures,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: checked={len(rows)} "
        f"counts={dict(counts)}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
