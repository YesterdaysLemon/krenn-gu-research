#!/usr/bin/env python3
"""Test whether the two rare q5_311 P4 slices already contradict a chart.

In the normalized q5_311 branch, mode zero has singleton colours
``(0,0,0,1,2)``.  Fixing mode-zero colour 1 or 2 therefore selects one
source row and leaves a deleted-row copy of the P4 permanent in the other
four modes.  The target requires each of those two P4 tensors to be a
nonzero decomposable tensor in a different target direction.

This probe keeps only the corresponding mixed coefficients.  It can
saturate either just the two rare pure coefficients or all three pure
coefficients; the latter still omits every majority-colour mixed equation.
``UNIT_IDEAL`` is an exact characteristic-zero certificate for the selected
chart, while any other outcome is inconclusive as an exclusion.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import generate_p5_one_partial_support_system as GENERATOR
import generate_p5_split_saturation_system as SPLIT
import p5_high_coordinate_tree_chart_cegar as HIGH
import p5_pair_support_semantics as SEMANTICS
import verify_p5_high_coordinate_chart_ledgers as LEDGER


def build_program(
    record: dict,
    include_majority_pure: bool = False,
    basis_algorithm: str = "slimgb",
    inverse_first: bool = False,
) -> tuple[str, str, dict]:
    if basis_algorithm not in ("slimgb", "std"):
        raise ValueError("unsupported Singular basis algorithm")
    supports = LEDGER.normalized_supports(
        record["closure_supports"]
    )
    tree = LEDGER.normalized_tree(record["gauge_tree"])
    if supports[0] != HIGH.BRANCH_BACKBONES["q5_311"]:
        raise ValueError("record is not in normalized q5_311 form")
    LEDGER.validate_forest(
        LEDGER.normalized_supports(record["supports"]),
        supports,
        tree,
    )

    edges = tuple(
        (mode, source, colour)
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in SEMANTICS.COLOURS
        if supports[mode][source] & (1 << colour)
    )
    tree_set = set(tree)
    if len(tree_set) != len(tree) or any(
        edge not in edges for edge in tree
    ):
        raise ValueError("gauge forest is not contained in the chart")
    free_edges = tuple(edge for edge in edges if edge not in tree_set)
    free_position = {
        edge: index for index, edge in enumerate(free_edges)
    }
    names = [f"u{index}" for index in range(len(free_edges))]
    one: GENERATOR.Expression = (
        Fraction(1),
        (0,) * len(free_edges),
    )

    def entry(
        mode: int,
        source: int,
        colour: int,
    ) -> GENERATOR.Expression | None:
        edge = (mode, source, colour)
        if edge in tree_set:
            return one
        position = free_position.get(edge)
        if position is None:
            return None
        exponent = [0] * len(free_edges)
        exponent[position] = 1
        return Fraction(1), tuple(exponent)

    def coefficient(colours: tuple[int, ...]) -> str:
        terms: dict[tuple[int, ...], Fraction] = {}
        for permutation in itertools.permutations(SEMANTICS.SOURCES):
            value = one
            for mode, source in enumerate(permutation):
                factor = entry(mode, source, colours[mode])
                if factor is None:
                    break
                value = GENERATOR.multiply(value, factor)
            else:
                terms[value[1]] = (
                    terms.get(value[1], Fraction(0)) + value[0]
                )
        return GENERATOR.polynomial_string(
            terms,
            names,
            set(),
        )

    mixed = []
    for colours in itertools.product(
        SEMANTICS.COLOURS,
        repeat=5,
    ):
        if colours[0] not in (1, 2) or len(set(colours)) == 1:
            continue
        polynomial = coefficient(colours)
        if polynomial != "0":
            mixed.append(polynomial)
    mixed = list(dict.fromkeys(mixed))
    pure_colours = (
        (0, 1, 2) if include_majority_pure else (1, 2)
    )
    pure = {
        colour: coefficient((colour,) * 5)
        for colour in pure_colours
    }
    if any(polynomial == "0" for polynomial in pure.values()):
        raise AssertionError("a required rare pure coefficient vanished")

    variables = names + ["z"]
    saturation = "*".join(
        f"({pure[colour]})" for colour in pure_colours
    )
    equations = mixed + [f"z*({saturation})-1"]
    program = "\n".join(
        [
            "// q5_311 simultaneous rare-colour P4 slices",
            f"// supports: {supports}",
            f"// gauge forest: {tree}",
            "// retained mode-zero colours: 1,2",
            f"// distinct rare mixed equations: {len(mixed)}",
            (
                "// saturated pure coefficients: "
                + ",".join(map(str, pure_colours))
            ),
            f"ring r=0,({','.join(variables)}),dp;",
            "option(redSB);",
            "ideal I=" + ",\n".join(equations) + ";",
            f"ideal G={basis_algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    safe_names = [
        f"v{index:02d}" for index in range(len(names))
    ]
    safe_name = dict(zip(names, safe_names, strict=True))

    def rename(expression: str) -> str:
        return SPLIT.IDENTIFIER_PATTERN.sub(
            lambda match: safe_name[match.group(0)],
            expression,
        )

    safe_mixed = [rename(polynomial) for polynomial in mixed]
    safe_pure = {
        colour: rename(polynomial)
        for colour, polynomial in pure.items()
    }
    inverse_names = [
        f"w{colour}" for colour in pure_colours
    ]
    split_variables = (
        inverse_names + safe_names
        if inverse_first
        else safe_names + inverse_names
    )
    split_program = "\n".join(
        [
            "// exact split saturation for q5_311 rare P4 slices",
            (
                "ring r=0,("
                + ",".join(split_variables)
                + "),dp;"
            ),
            "option(redSB);",
            "ideal I="
            + ",\n".join(
                [
                    *(
                        f"w{colour}*({safe_pure[colour]})-1"
                        for colour in pure_colours
                    ),
                    *safe_mixed,
                ]
            )
            + ";",
            f"ideal G={basis_algorithm}(I);",
            'if (size(G)==1 && G[1]==1) { "UNIT_IDEAL"; }',
            'else { "SURVIVOR"; size(G); vdim(G); }',
            "$;",
            "",
        ]
    )
    return program, split_program, {
        "closure_entries": len(edges),
        "gauge_forest_edges": len(tree),
        "variables": len(variables),
        "rare_mixed_equations": len(mixed),
        "saturated_pure_colours": pure_colours,
        "majority_mixed_equations": 0,
        "basis_algorithm": basis_algorithm,
        "split_inverse_variables_first": inverse_first,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--record-index",
        type=int,
        action="append",
        required=True,
    )
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--source-output", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--quiet-progress", action="store_true")
    parser.add_argument(
        "--split-only",
        action="store_true",
        help=(
            "skip the direct product saturation and run only the "
            "equivalent split-inverse formulation"
        ),
    )
    parser.add_argument(
        "--basis-algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    parser.add_argument(
        "--inverse-first",
        action="store_true",
        help="place split inverse variables before chart variables",
    )
    parser.add_argument(
        "--include-majority-pure",
        action="store_true",
        help=(
            "also require the majority pure coefficient to be nonzero "
            "while retaining only rare-colour mixed equations"
        ),
    )
    args = parser.parse_args()
    if any(index < 0 for index in args.record_index) or args.timeout <= 0:
        raise ValueError("invalid rare-slice probe arguments")
    if args.source_output and len(args.record_index) != 1:
        raise ValueError(
            "--source-output requires exactly one record index"
        )

    raw = args.state.read_bytes()
    state = json.loads(raw)
    if state.get("branch") != "q5_311":
        raise ValueError("rare-slice probe requires q5_311")
    records = state.get("records", [])
    if any(index >= len(records) for index in args.record_index):
        raise IndexError("record index is outside the state ledger")

    results = []
    for index in args.record_index:
        program, split_program, metadata = build_program(
            records[index],
            args.include_majority_pure,
            args.basis_algorithm,
            args.inverse_first,
        )
        if args.source_output:
            args.source_output.write_text(program, encoding="utf-8")
        direct = (
            {
                "status": "SKIPPED",
                "elapsed_seconds": 0.0,
            }
            if args.split_only
            else HIGH.run_singular(program, args.timeout)
        )
        split = None
        method = "direct"
        result = direct
        if direct["status"] != "UNIT_IDEAL":
            split = HIGH.run_singular(split_program, args.timeout)
            result = split
            if split["status"] == "UNIT_IDEAL":
                method = "split"
            else:
                method = "inconclusive"
        results.append(
            {
                "record_index": index,
                "verified": result["status"] == "UNIT_IDEAL",
                "method": method,
                "source_sha256": HIGH.sha256_text(program),
                "split_source_sha256": HIGH.sha256_text(
                    split_program
                ),
                "metadata": metadata,
                "direct_cas": direct,
                "split_cas": split,
                "cas": result,
            }
        )
        if not args.quiet_progress:
            print(
                json.dumps(
                    {
                        "record_index": index,
                        "status": result["status"],
                        "seconds": result["elapsed_seconds"],
                        "rare_mixed_equations": metadata[
                            "rare_mixed_equations"
                        ],
                    }
                ),
                flush=True,
            )

    payload = {
        "verified": all(result["verified"] for result in results),
        "scope": (
            "selected exact q5_311 charts under only the simultaneous "
            "rare-colour P4 slice equations"
        ),
        "state": args.state.as_posix(),
        "state_sha256": hashlib.sha256(raw).hexdigest(),
        "records_tested": len(results),
        "unit_ideals": sum(
            result["verified"] for result in results
        ),
        "inconclusive": sum(
            not result["verified"] for result in results
        ),
        "results": results,
        "global_conjecture_resolved": False,
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(
            json.dumps(
                {
                    "verified": payload["verified"],
                    "records_tested": payload["records_tested"],
                    "unit_ideals": payload["unit_ideals"],
                    "inconclusive": payload["inconclusive"],
                    "output": args.output.as_posix(),
                },
                indent=2,
            )
        )
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
