"""Find a direct full-only/one-extra contradiction on one support.

For an all-even full factor, every full-only amplitude is a product of
cycle binomials.  A forbidden amplitude with exactly one additional
matching rules out each cycle binomial occurring in its full-only part:
if that binomial vanished, the one extra nonzero monomial would remain.
This script searches for a full-only equation whose every cycle
binomial is ruled out in that way.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n14")

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_even_cycle_double_pair_fork import (
    activity_arrays,
)
from analyze_fourteen_vertex_forced_slice_factor_cegar import (
    extras_at,
    full_containing_indices,
)
from analyze_fourteen_vertex_unforced_factor_choice_cegar import (
    SparseRelation,
    cycle_relation,
    is_forbidden_equation,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument(
        "--max-certificates",
        type=int,
        default=1,
        help="retain this many distinct direct cores from the same support",
    )
    parser.add_argument(
        "--extra-output-prefix",
        type=Path,
        help=(
            "when more than one core is requested, write cores after the "
            "first as PREFIX_1.json, PREFIX_2.json, and so on"
        ),
    )
    parser.add_argument(
        "--unit-origins-per-relation",
        type=int,
        default=1,
        help=(
            "retain this many distinct one-extra witnesses for each "
            "cycle relation before forming direct cores"
        ),
    )
    parser.add_argument(
        "--spread-base-equations",
        action="store_true",
        help=(
            "for multi-certificate runs, first seek one valid core in "
            "each evenly spaced bucket of full-only equations"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.max_certificates < 1:
        raise ValueError("--max-certificates must be positive")
    if args.unit_origins_per_relation < 1:
        raise ValueError(
            "--unit-origins-per-relation must be positive"
        )
    if args.max_certificates > 1 and args.extra_output_prefix is None:
        raise ValueError(
            "--extra-output-prefix is required for multiple certificates"
        )
    started = time.perf_counter()

    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    if (
        sum(lengths) != 14
        or len(cycles) < 2
        or any(len(cycle) % 2 for cycle in cycles)
    ):
        raise ValueError("analysis requires an all-even partition")
    baseline = 1 << len(cycles)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    factors = tuple(
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    )
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    if (
        any(len(factor) != 7 for factor in factors)
        or len(labels) != 21
        or set(labels) & set(full_edges)
    ):
        raise AssertionError("singleton support changed")
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if len(full_only) != baseline:
        raise AssertionError("full-only matching count changed")
    counts, slots, total_extensions = activity_arrays(
        matchings, labels, baseline + 1
    )
    base_indices = [
        int(value)
        for value in full_containing_indices(
            counts, slots, full_only, baseline
        )
        if is_forbidden_equation(int(value))
    ]
    one_extra_indices = [
        int(value)
        for value in full_containing_indices(
            counts, slots, full_only, baseline + 1
        )
        if is_forbidden_equation(int(value))
    ]

    unit_origins: dict[
        SparseRelation, list[tuple[int, int, int]]
    ] = {}
    for equation in one_extra_indices:
        extra = extras_at(
            equation, baseline + 1, slots, full_only
        )
        if len(extra) != 1:
            raise AssertionError("one-extra row changed")
        colouring = engine.indexed_colouring(equation)
        for cycle_id, cycle in enumerate(cycles):
            signature = cycle_relation(
                cycle, colouring, labels, full_edges
            )
            origins = unit_origins.setdefault(signature, [])
            origin = (equation, extra[0], cycle_id)
            if (
                len(origins) < args.unit_origins_per_relation
                and origin not in origins
            ):
                origins.append(origin)
    unit_relations_by_cycle = [
        sum(
            1
            for origins in unit_origins.values()
            if origins and origins[0][2] == cycle_id
        )
        for cycle_id in range(len(cycles))
    ]

    certificates = []
    certificate_keys = set()

    def collect_at_equation(
        equation: int, maximum_new: int | None = None
    ) -> int:
        before = len(certificates)
        colouring = engine.indexed_colouring(equation)
        option_rows = []
        for cycle_id, cycle in enumerate(cycles):
            signature = cycle_relation(
                cycle, colouring, labels, full_edges
            )
            origins = unit_origins.get(signature)
            if not origins:
                return 0
            option_rows.append((cycle_id, signature, origins))
        for selected_origins in itertools.product(
            *(row[2] for row in option_rows)
        ):
            rows = []
            for (
                cycle_id,
                signature,
                _,
            ), (
                unit_equation,
                extra_matching,
                unit_cycle_id,
            ) in zip(option_rows, selected_origins, strict=True):
                rows.append(
                    {
                        "base_cycle_id": cycle_id,
                        "relation_signature": [
                            list(item) for item in signature
                        ],
                        "one_extra_equation_index": unit_equation,
                        "one_extra_colouring": list(
                            engine.indexed_colouring(unit_equation)
                        ),
                        "one_extra_matching_id": extra_matching,
                        "one_extra_cycle_id": unit_cycle_id,
                    }
                )
            key = (
                equation,
                tuple(
                    int(row["one_extra_equation_index"])
                    for row in rows
                ),
            )
            if key in certificate_keys:
                continue
            certificate_keys.add(key)
            certificates.append({
                "certificate_mode": (
                    "full_only_clause_blocked_by_one_extra_units"
                ),
                "full_only_equation_index": equation,
                "full_only_colouring": list(colouring),
                "cycle_rows": rows,
                "distinct_cycle_relations": len(
                    {
                        tuple(
                            tuple(map(int, item))
                            for item in row["relation_signature"]
                        )
                        for row in rows
                    }
                ),
            })
            if (
                len(certificates) >= args.max_certificates
                or (
                    maximum_new is not None
                    and len(certificates) - before >= maximum_new
                )
            ):
                break
        return len(certificates) - before

    if args.spread_base_equations and args.max_certificates > 1:
        bucket_count = min(args.max_certificates, len(base_indices))
        for bucket in range(bucket_count):
            start = bucket * len(base_indices) // bucket_count
            stop = (bucket + 1) * len(base_indices) // bucket_count
            for equation in base_indices[start:stop]:
                if collect_at_equation(equation, maximum_new=1):
                    break
            if len(certificates) >= args.max_certificates:
                break

    # Fill any empty buckets, or retain the historical earliest-first
    # behaviour when spreading is disabled. Keys keep the fallback
    # deterministic and duplicate-free.
    if len(certificates) < args.max_certificates:
        for equation in base_indices:
            collect_at_equation(equation)
            if len(certificates) >= args.max_certificates:
                break

    status = (
        "one_extra_cycle_core"
        if certificates
        else "one_extra_cycle_core_absent"
    )
    base_payload = {
        "status": status,
        "scope": (
            "one fixed all-even order-14 equality support and the "
            "full-only/one-extra direct cycle-factor mechanism"
        ),
        "exploration": str(args.exploration),
        "exploration_sha256": sha256(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": len(full_only),
        "matching_extensions_accumulated": total_extensions,
        "forbidden_full_only_equations": len(base_indices),
        "forbidden_one_extra_equations": len(one_extra_indices),
        "one_extra_unit_relations": len(unit_origins),
        "one_extra_unit_relations_by_cycle": (
            unit_relations_by_cycle
        ),
        "one_extra_unit_origins": sum(
            len(origins) for origins in unit_origins.values()
        ),
        "unit_origins_per_relation": (
            args.unit_origins_per_relation
        ),
        "spread_base_equations": args.spread_base_equations,
        "certificates_requested": args.max_certificates,
        "certificates_found": len(certificates),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_verified": (
            bool(certificates)
        ),
        "global_conjecture_resolved": False,
    }
    payload = {
        **base_payload,
        "certificate": certificates[0] if certificates else None,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    if len(certificates) > 1:
        assert args.extra_output_prefix is not None
        for certificate_id, certificate in enumerate(
            certificates[1:], start=1
        ):
            extra_path = Path(
                f"{args.extra_output_prefix}_{certificate_id}.json"
            )
            extra_path.parent.mkdir(parents=True, exist_ok=True)
            extra_path.write_text(
                json.dumps(
                    {
                        **base_payload,
                        "certificate_index": certificate_id,
                        "certificate": certificate,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
