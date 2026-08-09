#!/usr/bin/env python3
"""Primary verifier for the support-four P_5 contraction restriction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md"
PERMUTATIONS = tuple(itertools.permutations(range(5)))
TARGET_TUPLES = tuple(itertools.product(range(3), repeat=4))

INTEGER_MAPS = (
    sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [-1, -1, 0],
            [0, 0, -1],
        ]
    ),
    sp.Matrix(
        [
            [1, 1, -2],
            [-2, 1, 1],
            [1, -2, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ),
    sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, -1, -1],
            [-1, 0, 0],
        ]
    ),
    sp.Matrix(
        [
            [-1, -1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, 1, -1],
            [0, -2, 0],
        ]
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contracted_coefficient(
    maps: tuple[sp.Matrix, ...], colours: tuple[int, ...]
) -> sp.Expr:
    # The fixed first-mode vector is (1,1,1,1,0).  Equivalently, a
    # remaining injection is active iff its missing coordinate is < 4.
    result = 0
    for injection in itertools.permutations(range(5), 4):
        missing = next(
            coordinate
            for coordinate in range(5)
            if coordinate not in injection
        )
        if missing == 4:
            continue
        result += sp.prod(
            maps[mode][injection[mode], colours[mode]]
            for mode in range(4)
        )
    return sp.expand(result)


def family_maps(u: sp.Expr, v: sp.Expr, w: sp.Expr) -> tuple[sp.Matrix, ...]:
    parameters = {0: u, 2: v, 3: w}
    special_colours = {0: 2, 2: 0, 3: 1}
    distinguished_coordinate = {0: 1, 1: 2, 2: 0}
    maps = []
    for mode in range(4):
        columns = []
        for colour in range(3):
            if mode == 1:
                source = [sp.Integer(1)] * 3
                source[distinguished_coordinate[colour]] = -2
                source.append(sp.Integer(1))
                alpha = sp.Integer(1)
            else:
                parameter = parameters[mode]
                source = [parameter] * 3
                source[distinguished_coordinate[colour]] = 1
                source.append(
                    -parameter
                    if colour == special_colours[mode]
                    else -1
                )
                alpha = (
                    parameter - 1
                    if colour == special_colours[mode]
                    else 0
                )
            columns.append(sp.Matrix(source + [alpha]))
        maps.append(sp.Matrix.hstack(*columns))
    return tuple(maps)


def main() -> None:
    assert [matrix.rank() for matrix in INTEGER_MAPS] == [3, 3, 3, 3]
    coefficients = {
        colours: contracted_coefficient(INTEGER_MAPS, colours)
        for colours in TARGET_TUPLES
    }
    nonzero_coefficients = {
        colours: coefficient
        for colours, coefficient in coefficients.items()
        if coefficient != 0
    }
    assert nonzero_coefficients == {
        (0, 0, 0, 0): 12,
        (1, 1, 1, 1): 12,
        (2, 2, 2, 2): 12,
    }

    # Symbolically reconstruct the two-parameter family.
    u, v, w = sp.symbols("u v w")
    relation = sp.expand(
        u * v * w - u * v - u * w - u - v * w - v - w - 1
    )
    parametric_maps = family_maps(u, v, w)
    off_diagonal_coefficients = 0
    diagonal_quotients = set()
    for colours in TARGET_TUPLES:
        coefficient = contracted_coefficient(parametric_maps, colours)
        _, remainder = sp.div(coefficient, relation, w)
        remainder = sp.factor(remainder)
        if len(set(colours)) == 1:
            diagonal_quotients.add(
                sp.factor(
                    (coefficient + 12 * (u + v + w)) / relation
                )
            )
        else:
            off_diagonal_coefficients += 1
            assert remainder == 0
    assert off_diagonal_coefficients == 78
    assert diagonal_quotients == {-4}
    assert family_maps(0, 0, -1) == INTEGER_MAPS

    output = {
        "verified": True,
        "field": "C",
        "integer_map_ranks": [matrix.rank() for matrix in INTEGER_MAPS],
        "target_coefficients_checked": len(coefficients),
        "nonzero_target_coefficients": {
            ",".join(map(str, colours)): str(coefficient)
            for colours, coefficient in nonzero_coefficients.items()
        },
        "family_relation": str(relation),
        "family_off_diagonal_coefficients_checked": (
            off_diagonal_coefficients
        ),
        "family_diagonal_remainder": "-12*(u + v + w)",
        "support_four_contraction_subrank_lower_bound": 3,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "support_four_p5_contraction_restriction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
