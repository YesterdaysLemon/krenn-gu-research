#!/usr/bin/env python3
"""Enumerate viable exact-k-partial P5 supports up to fixed-shape symmetry."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


ROOT = Path(__file__).resolve().parent
DRIVER_PATH = ROOT / "tmp" / "probe_p5_max3_coordinate_support.py"
SPEC = importlib.util.spec_from_file_location("p5_driver", DRIVER_PATH)
DRIVER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(DRIVER)
P5 = DRIVER.P5


def checkpoint(
    path: Path,
    shape: str,
    partial_cells: int,
    status: str,
    cases: list[dict],
    available_percent: float,
) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            {
                "status": status,
                "scope": (
                    "support-semantics-viable "
                    f"exact-{partial_cells}-partial supports "
                    "up to fixed-shape symmetry"
                ),
                "shape": shape,
                "partial_cells": partial_cells,
                "support_orbits": len(cases),
                "available_percent": round(available_percent, 3),
                "cases": cases,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=tuple(DRIVER.SHAPES), required=True)
    parser.add_argument(
        "--partial-cells",
        type=int,
        choices=tuple(range(1, 11)),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--limit",
        type=int,
        default=100_000,
        help="maximum new support orbits in this invocation",
    )
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=1_000,
        help="write a resumable checkpoint after this many total orbits",
    )
    args = parser.parse_args()
    if args.limit <= 0:
        raise ValueError("--limit must be positive")
    if args.checkpoint_every <= 0:
        raise ValueError("--checkpoint-every must be positive")
    if not 15 <= args.min_available_percent < 100:
        raise ValueError("memory floor must be at least 15 and below 100")

    allowed = P5.finite_field_local_signatures()
    automorphisms = DRIVER.shape_automorphisms(args.shape)
    cnf, pool = P5.build_cnf(
        allowed,
        double_lex=False,
        pair_hierarchy=True,
    )
    shape_lex_leaders = DRIVER.add_shape_lex_leaders(
        cnf, pool, args.shape, automorphisms
    )

    for mode in P5.MODES:
        required_noncoordinate = set(DRIVER.SHAPES[args.shape][mode])
        for pattern_index, signature in enumerate(allowed):
            observed_noncoordinate = {
                source
                for source, mask in enumerate(signature[0])
                if mask not in (1, 2, 4)
            }
            if observed_noncoordinate != required_noncoordinate:
                cnf.append(
                    [-pool.id(("local_pattern", mode, pattern_index))]
                )

    missing_literals = [
        -pool.id(P5.entry_key(mode, source, colour))
        for mode, sources in enumerate(DRIVER.SHAPES[args.shape])
        for source in sources
        for colour in P5.COLOURS
    ]
    if len(missing_literals) != 30:
        raise AssertionError("noncoordinate entry count changed")
    exact_k = CardEnc.equals(
        lits=missing_literals,
        bound=args.partial_cells,
        vpool=pool,
        encoding=EncType.seqcounter,
    )
    cnf.extend(exact_k.clauses)

    cases = []
    if args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8"))
        if (
            previous.get("shape") != args.shape
            or previous.get("partial_cells") != args.partial_cells
        ):
            raise ValueError("checkpoint scope mismatch")
        cases = list(previous.get("cases", []))

    print(
        json.dumps(
            {
                "shape": args.shape,
                "partial_cells": args.partial_cells,
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "shape_automorphisms": len(automorphisms),
                "shape_lex_leaders": shape_lex_leaders,
                "preloaded_support_orbits": len(cases),
                "available_percent": round(
                    DRIVER.available_memory_percent(), 3
                ),
                "min_available_percent": args.min_available_percent,
            }
        ),
        flush=True,
    )

    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        seen = set()
        for case in cases:
            supports = tuple(tuple(row) for row in case["supports"])
            if supports in seen:
                raise ValueError("duplicate checkpoint support")
            seen.add(supports)
            solver.add_clause(P5.exact_support_clause(pool, supports))

        for _ in range(args.limit):
            available = DRIVER.available_memory_percent()
            if available < args.min_available_percent:
                checkpoint(
                    args.output,
                    args.shape,
                    args.partial_cells,
                    "PAUSED_MEMORY_FLOOR",
                    cases,
                    available,
                )
                print(
                    json.dumps(
                        {
                            "status": "PAUSED_MEMORY_FLOOR",
                            "support_orbits": len(cases),
                            "available_percent": round(available, 3),
                        }
                    ),
                    flush=True,
                )
                return
            if not solver.solve():
                checkpoint(
                    args.output,
                    args.shape,
                    args.partial_cells,
                    "COMPLETE",
                    cases,
                    available,
                )
                print(
                    json.dumps(
                        {
                            "status": "COMPLETE",
                            "support_orbits": len(cases),
                        }
                    ),
                    flush=True,
                )
                return

            model = solver.get_model()
            positive = {literal for literal in model if literal > 0}
            supports = P5.supports_from_model(pool, model)
            observed_partial_cells = sum(
                mask in (3, 5, 6)
                for row in supports
                for mask in row
            )
            if observed_partial_cells != args.partial_cells:
                raise AssertionError(
                    "exact-k cardinality failed: "
                    f"{observed_partial_cells} != {args.partial_cells}"
                )
            if supports in seen:
                raise AssertionError("support blocker failed")
            signature_indices = [
                next(
                    index
                    for index in range(len(allowed))
                    if pool.id(("local_pattern", mode, index)) in positive
                )
                for mode in P5.MODES
            ]
            seen.add(supports)
            cases.append(
                {
                    "shape": args.shape,
                    "orbit_index": len(cases),
                    "supports": supports,
                    "witness_signature_indices": signature_indices,
                }
            )
            solver.add_clause(P5.exact_support_clause(pool, supports))
            if len(cases) % args.checkpoint_every == 0:
                checkpoint(
                    args.output,
                    args.shape,
                    args.partial_cells,
                    "IN_PROGRESS",
                    cases,
                    available,
                )
                print(
                    json.dumps(
                        {
                            "support_orbits": len(cases),
                            "available_percent": round(available, 3),
                        }
                    ),
                    flush=True,
                )

    checkpoint(
        args.output,
        args.shape,
        args.partial_cells,
        "LIMIT_REACHED",
        cases,
        DRIVER.available_memory_percent(),
    )
    print(
        json.dumps(
            {
                "status": "LIMIT_REACHED",
                "support_orbits": len(cases),
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
