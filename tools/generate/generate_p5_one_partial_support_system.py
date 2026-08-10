#!/usr/bin/env python3
"""Generate the exact one-partial P5 support system for Singular."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.p5_support_system import generate  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", required=True)
    parser.add_argument("--indices", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--partial-cells",
        type=int,
        choices=tuple(range(0, 11)),
        default=1,
    )
    parser.add_argument(
        "--coordinate-backbone-closure",
        action="store_true",
    )
    parser.add_argument(
        "--pure-saturation-only",
        action="store_true",
    )
    parser.add_argument(
        "--gauge-tree",
        help=(
            "optional Python literal containing the 19 "
            "(mode, source, colour) gauge-tree entries"
        ),
    )
    parser.add_argument(
        "--allow-arbitrary-support",
        action="store_true",
    )
    parser.add_argument(
        "--order",
        choices=("dp", "lp", "Dp"),
        default="dp",
    )
    parser.add_argument(
        "--algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    args = parser.parse_args()
    supports = tuple(
        tuple(map(int, row))
        for row in ast.literal_eval(args.supports)
    )
    indices = tuple(map(int, args.indices.split(",")))
    gauge_tree = (
        tuple(
            tuple(map(int, edge))
            for edge in ast.literal_eval(args.gauge_tree)
        )
        if args.gauge_tree is not None
        else None
    )
    program, metadata = generate(
        supports,
        indices,
        expected_partial_cells=args.partial_cells,
        coordinate_backbone_closure=args.coordinate_backbone_closure,
        pure_saturation_only=args.pure_saturation_only,
        gauge_tree_edges=gauge_tree,
        allow_arbitrary_support=args.allow_arbitrary_support,
        monomial_order=args.order,
        algorithm=args.algorithm,
    )
    args.output.write_text(program, encoding="utf-8", newline="\n")
    print(metadata)


if __name__ == "__main__":
    main()
