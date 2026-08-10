#!/usr/bin/env python3
"""Independent apolar audit for the two-all-normal obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def derivative(polynomial, variables, direction):
    return sp.expand(
        sum(
            coefficient * sp.diff(polynomial, variable)
            for coefficient, variable in zip(
                direction,
                variables,
                strict=True,
            )
        )
    )


def main() -> None:
    x0, x1, x2, x3, x4 = sp.symbols("x0 x1 x2 x3 x4")
    variables = (x0, x1, x2, x3, x4)
    u0 = (1, 1, 0, 0, 0)
    h0 = (1, -1, 0, 0, 0)
    u1 = (0, 0, 1, 1, 0)
    h1 = (0, 0, 1, -1, 0)
    h2 = (0, 0, 0, 0, 1)
    f0 = (x0 + x1) * x2 * x3 * x4
    f1 = x0 * x1 * (x2 + x3) * x4
    f2 = x0 * x1 * x2 * x3

    residuals = (
        derivative(derivative(f0, variables, h2), variables, h1),
        derivative(derivative(f1, variables, h2), variables, h0),
        derivative(derivative(f2, variables, h1), variables, h0),
    )
    expected = (
        -(x0 + x1) * (x2 - x3),
        -(x0 - x1) * (x2 + x3),
        (x0 - x1) * (x2 - x3),
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(residuals, expected, strict=True)
    )

    dependency_edges = ((0, 3), (1, 2), (1, 3))
    pair_component_counts = []
    for pair in itertools.combinations(dependency_edges, 2):
        vertices = [{index} for index in range(4)]
        for left, right in pair:
            merged = next(group for group in vertices if left in group)
            other = next(group for group in vertices if right in group)
            if merged is not other:
                merged |= other
                vertices.remove(other)
        assert len(vertices) == 2
        pair_component_counts.append(len(vertices))

    output = {
        "audited": True,
        "field": "C",
        "method": "independent apolar derivatives and graph components",
        "bilinear_residual_polynomials": [str(value) for value in residuals],
        "two_edge_subsets_checked": len(pair_component_counts),
        "components_after_any_two_dependencies": pair_component_counts,
        "ambient_maps_enumerated": 0,
        "monotone_cover_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "source contractions and dependency-rank obstruction",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_two_all_normal_modes_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
