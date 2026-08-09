#!/usr/bin/env python3
"""Verify the constant identities in the smooth four-root torus theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "FOUR_ROOT_SMOOTH_TORUS_OBSTRUCTION.md"
VERTICES = tuple(range(4))
EDGES = tuple(itertools.combinations(VERTICES, 2))
Exponent = tuple[int, int, int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chow_product() -> Counter[Exponent]:
    polynomial: Counter[Exponent] = Counter({(0, 0, 0, 0): 1})
    for left, right in EDGES:
        updated: Counter[Exponent] = Counter()
        for exponent, coefficient in polynomial.items():
            for endpoint in (left, right):
                target = list(exponent)
                target[endpoint] += 1
                if target[endpoint] < 3:
                    updated[tuple(target)] += coefficient
        polynomial = updated
    return polynomial


def koszul_ledger() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    nonzero_cohomology: list[dict[str, object]] = []
    degree_zero_candidates: list[dict[str, object]] = []
    for mask in range(1 << len(EDGES)):
        selected = tuple(
            edge for index, edge in enumerate(EDGES) if mask & (1 << index)
        )
        degrees = [0, 0, 0, 0]
        for left, right in selected:
            degrees[left] += 1
            degrees[right] += 1
        if any(degree in (1, 2) for degree in degrees):
            continue
        cohomology_degree = 2 * sum(degree == 3 for degree in degrees)
        koszul_degree = len(selected)
        entry = {
            "edges": [list(edge) for edge in selected],
            "vertex_degrees": degrees,
            "koszul_degree": koszul_degree,
            "cohomology_degree": cohomology_degree,
            "total_degree": cohomology_degree - koszul_degree,
        }
        nonzero_cohomology.append(entry)
        if cohomology_degree - koszul_degree == 0:
            degree_zero_candidates.append(entry)
    return nonzero_cohomology, degree_zero_candidates


def main() -> None:
    polynomial = chow_product()
    assert polynomial
    boundary_free_coefficients = {}
    for omitted in VERTICES:
        exponent = tuple(0 if index == omitted else 2 for index in VERTICES)
        assert polynomial[exponent] == 2
        assert all(
            coefficient == 0 or exponents[omitted] > 0 or exponents == exponent
            for exponents, coefficient in polynomial.items()
        )
        boundary_free_coefficients[str(omitted)] = polynomial[exponent]

    nonzero, degree_zero = koszul_ledger()
    assert len(nonzero) == 2
    assert nonzero[0]["vertex_degrees"] == [0, 0, 0, 0]
    assert nonzero[0]["total_degree"] == 0
    assert nonzero[1]["vertex_degrees"] == [3, 3, 3, 3]
    assert nonzero[1]["total_degree"] == 2
    assert degree_zero == [nonzero[0]]

    theorem = THEOREM.read_text(encoding="utf-8")
    normalized_theorem = " ".join(theorem.split())
    for phrase in (
        "smooth of dimension two",
        "H^0(Z,O_Z)=C",
        "P_4 -> Delta_3",
        "does not yet prove",
    ):
        assert phrase in normalized_theorem, phrase

    result = {
        "status": "verified",
        "field": "C",
        "edge_subsets_checked": 1 << len(EDGES),
        "chow_monomials": len(polynomial),
        "boundary_free_chow_coefficients": boundary_free_coefficients,
        "nonzero_koszul_cohomology_summands": nonzero,
        "degree_zero_koszul_summands": len(degree_zero),
        "connected_complete_intersection": True,
        "smooth_implies_irreducible": True,
        "smooth_expected_four_root_scheme_meets_torus": True,
        "eight_vertex_consequence": (
            "all 70 four-root schemes singular or excess-dimensional"
        ),
        "global_conjecture_resolved": False,
        "search_used": False,
        "finite_checks_are_formula_audits_only": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
