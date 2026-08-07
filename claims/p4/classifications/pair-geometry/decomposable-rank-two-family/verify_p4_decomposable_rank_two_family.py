#!/usr/bin/env python3
"""Symbolically verify the exact rank-two P4 compression family."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_DECOMPOSABLE_RANK_TWO_FAMILY.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.factor(
        sp.together(
            sum(
                sp.prod(rows[row][permutation[row]] for row in range(4))
                for permutation in PERMUTATIONS
            )
        )
    )


def row_minor(
    upper: tuple[sp.Expr, ...],
    lower: tuple[sp.Expr, ...],
    first: int,
    second: int,
) -> sp.Expr:
    return sp.factor(
        upper[first] * lower[second]
        - upper[second] * lower[first]
    )


def main() -> None:
    epsilon, iota = sp.symbols("epsilon iota", nonzero=True)
    ell, jay, chi = sp.symbols("ell jay chi")
    gamma = epsilon * iota * ell

    upper = (
        (0, 1, (chi + gamma) / epsilon, chi),
        (0, 0, 1, epsilon),
        (0, 1, 0, gamma),
        (1, 0, iota, 0),
    )
    lower = (
        (1, jay, 0, -epsilon * iota * (1 + ell * jay)),
        (ell, 1, -iota * ell, -gamma),
        (-1 / iota, 0, 1, 0),
        (0, 0, -1 / epsilon, 1),
    )

    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = tuple(
            lower[index] if bit else upper[index]
            for index, bit in enumerate(bits)
        )
        coefficients["".join(map(str, bits))] = permanent(rows)

    assert sp.simplify(
        coefficients["0000"] - 2 * (chi + gamma)
    ) == 0
    assert all(
        value == 0
        for word, value in coefficients.items()
        if word != "0000"
    )

    rank_minors = (
        row_minor(upper[0], lower[0], 0, 1),
        row_minor(upper[1], lower[1], 1, 2),
        row_minor(upper[2], lower[2], 1, 2),
        row_minor(upper[3], lower[3], 0, 3),
    )
    assert rank_minors == (-1, -1, 1, 1)

    substitutions = {
        epsilon: 1,
        iota: 1,
        ell: 1,
        jay: 0,
        chi: 0,
    }
    integer_coefficients = {
        word: int(value.subs(substitutions))
        for word, value in coefficients.items()
    }
    expected = {word: 0 for word in coefficients}
    expected["0000"] = 2
    assert integer_coefficients == expected

    output = {
        "verified": True,
        "field": "C",
        "family_parameters": ["e", "i", "l", "j", "c"],
        "nonvanishing_conditions": ["e", "i", "c+e*i*l"],
        "local_ranks": [2, 2, 2, 2],
        "rank_witness_minors": [int(value) for value in rank_minors],
        "pure_coefficient": "2*(c+e*i*l)",
        "mixed_coefficients_checked": 15,
        "mixed_coefficients_nonzero": 0,
        "integer_point_pure_coefficient": integer_coefficients["0000"],
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_decomposable_rank_two_family_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
